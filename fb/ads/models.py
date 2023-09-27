import os.path

from django.db import models
from urllib.parse import urlparse
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
import re
from django.utils import timezone
from parsers import FbGroupPage
import requests as req
from django.core.files.base import ContentFile
from io import StringIO
from django.db.models import Q
import http.cookiejar

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5'
}

def remove_if_exists(path):
    if os.path.exists(path):
        os.remove(path)


def load_netscape_cookies(cookie_file):
    jar = http.cookiejar.MozillaCookieJar(cookie_file)
    jar.load()
    return jar


class KeyWord(models.Model):
    word = models.CharField(
        max_length=30,
        unique=True,
        validators=[RegexValidator(regex='([A-Za-z]){3,30}', message='Incorrect eng key word')])

    def __str__(self):
        return self.word


class ActualGroupManager(models.Manager):
    def get_queryset(self):
        qs = FbGroup.objects.exclude(Q(email='') | Q(name='')).filter(last_ad_date=timezone.now().date())
        return qs


class FullFbGroupManager(models.Manager):

    def get_queryset(self):
        qs = FbGroup.objects.exclude(Q(email='') | Q(name=''))
        return qs


class EmptyGroupManager(models.Manager):

    def get_queryset(self):
        qs = FbGroup.objects.filter(email='', name='')
        return qs


class NotLoadedGroupManager(models.Manager):
    def get_queryset(self):
        qs = FbGroup.objects.filter(status=FbGroup.NOT_LOADED)
        return qs


class FbGroup(models.Model):
    objects = models.Manager()
    full_objects = FullFbGroupManager()
    empty_objects = EmptyGroupManager()
    not_loaded_objects = NotLoadedGroupManager()
    actual_objects = ActualGroupManager()

    FB_GROUP_PATTERN = 'http[s]?://facebook.com/..{0,100}'
    REQ_HTML_DIR = '/home/vlad/PycharmProjects/FbSearcher/fb/media/req_html_data'

    NOT_LOADED = 'not_loaded'
    NEED_LOGIN = 'need_login'
    COLLECTED = 'collected'
    STATUSES = (
        (NOT_LOADED, 'Не загружен'),
        (NEED_LOGIN, 'Нужен вход'),
        (COLLECTED, 'Cобран'),
    )

    GROUP_DOMAIN = 'facebook.com'

    group_id = models.CharField(
        max_length=255,
        primary_key=True,
    )
    name = models.CharField(
        max_length=255,
        blank=True,
    )
    email = models.EmailField(
        blank=True,
    )
    address = models.CharField(
        max_length=255,
        blank=True,
    )
    status = models.CharField(choices=STATUSES, default=NOT_LOADED, max_length=15)

    created = models.DateField(
        auto_now_add=True,
    )
    last_ad_date = models.DateField(default=timezone.now)
    req_html_data = models.FileField(upload_to='req_html_data', blank=True)

    def __str__(self):
        return f'<FbGroup> {self.url}'

    @property
    def url(self):
        return f'https://www.facebook.com/profile.php?id={self.pk}'
        # return f'https://facebook.com/{self.pk}/'

    @staticmethod
    def global_stat():
        print('All:', FbGroup.objects.count())
        print('Actual:', FbGroup.actual_objects.count())
        print('Full:', FbGroup.full_objects.count())
        print('Empty:', FbGroup.empty_objects.count())
        print('Not loaded:', FbGroup.not_loaded_objects.count())

    @staticmethod
    def fb_group_url_to_id(url):
        url = urlparse(url).path
        if url.startswith('/'):
            url = url[1:]
        if url.endswith('/'):
            url = url[:-1]
        return url

    @staticmethod
    def update_db_by_group_ids(ids: iter) -> dict:
        print('update_db_by_group_ids')
        new_count = 0
        updated = 0
        for group_id in ids:
            group_model, created = FbGroup.objects.update_or_create(
                group_id=group_id,
                defaults={'last_ad_date': timezone.now().date()},
            )
            if created:
                new_count += 1
            else:
                updated += 1
        result = {
            'new': new_count,
            'updated': updated,
        }
        return result

    def get_group_req_html(self, cookies_path, log_html_data=True, ) -> str:
        """Получить исходный код страницы группы"""
        res = req.get(self.url, headers=headers, cookies=load_netscape_cookies(cookies_path))
        if res.status_code == 200:
            if log_html_data:
                self.log_html_source_file(html=res.text)
            return res.text
        else:
            print('Error req', res.status_code, self)
            return ''

    def log_html_source_file(self, html):
        if self.req_html_data:
            if os.path.exists(self.req_html_data.path):
                os.remove(self.req_html_data.path)
        file = ContentFile(html)
        self.req_html_data.save(f'{self.pk}.html', file)

    def update_group_info(self, cookies_path):
        html = self.get_group_req_html(cookies_path)
        if html:
            page = FbGroupPage(html)

            if page.is_login_form:
                self.status = self.NEED_LOGIN
                print('NEED_LOGIN', self)
            else:
                page()
                self.email = page.result.pop('group_email', self.email)
                self.name = page.result.pop('group_name', self.name)
                self.status = self.COLLECTED
                print('GOOD', self, self.email, self.name)
            self.save()

    def log_req_data(self, html):
        if self.req_html_data:
            remove_if_exists(self.req_html_data.path)
        file = ContentFile(html)
        file_name = f'{self.pk}.html'
        self.req_html_data.save(file_name, file, encodings='utf-8')

    @staticmethod
    def clean_data():
        FbGroup.objects.all().update(name='', email='', status=FbGroup.NOT_LOADED)




class ThreadCounter(models.Model):
    name = models.CharField(max_length=20,primary_key=True)
    count = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    def stat(self):
        delta = self.last_update - self.created
        print(self, f'AVG: {round(int(self.count) / delta.total_seconds(),1)}Count:{self.count} start:{self.created} last:{self.last_update}', )


    @staticmethod
    def clean_counters():
        ThreadCounter.objects.bulk_update(count=0)
