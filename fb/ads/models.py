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
import shutil

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
    title = models.CharField(
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

    def update(self, data:dict):
        self.name = data.get('name', self.name)
        self.email = data.get('email', self.email)
        self.title = data.get('title', self.title)
        self.status = FbGroup.COLLECTED
        self.save()

    def log_req_data(self, html):
        if self.req_html_data:
            remove_if_exists(self.req_html_data.path)
        file = ContentFile(html)
        file_name = f'{self.pk}.html'
        self.req_html_data.save(file_name, file)

    @staticmethod
    def clean_data():
        FbGroup.objects.all().update(name='', email='', status=FbGroup.NOT_LOADED, req_html_data='', title='')




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


class FbPagExample(models.Model):

    PAGES_TYPES = [
        ('fb_group', 'Группа'),
        ('fb_main', 'Главная'),
    ]
    type = models.CharField(max_length=30, blank=True, choices=PAGES_TYPES)
    name = models.CharField(max_length=255)
    desc = models.CharField(max_length=255)
    template = models.FileField(upload_to='fb_pages_examples')
    orig_url = models.URLField(blank=True)
    is_auth = models.BooleanField(verbose_name='Выполнен ли вход')

    def __str__(self):
        return self.name