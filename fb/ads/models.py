import os.path
import csv
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
import time
from parsers import FbGroupPageNoAuth
from requests.exceptions import ConnectTimeout, ProxyError, ReadTimeout, ConnectionError, RequestException
from django.db.utils import OperationalError
from requests.models import PreparedRequest
from datetime import datetime, timedelta
from django.conf import settings

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
    FB_LIB_URL = 'https://www.facebook.com/ads/library/'
    URL_PARAMS = {'active_status': 'all',
                  # 'ad_type': 'political_and_issue_ads',
                  'ad_type': 'all',
                  'country': None,
                  'q': None,
                  'sort_data[direction]': 'desc',
                  'sort_data[mode]': 'relevancy_monthly_grouped',
                  'search_type': 'keyword_unordered',
                  'media_type': 'all',
                  'start_date[min]': None,
                  'start_date[max]': '',
                  'publisher_platforms[0]': 'facebook',
                  }
    number_in_dict = models.IntegerField(default=0)
    word = models.CharField(
        max_length=30,
        primary_key=True,
        validators=[RegexValidator(regex='([A-Za-z]){1,30}', message='Incorrect eng key word')])
    ru_word = models.CharField(
        max_length=100,
        blank=True,
    )
    ads_count_policy = models.PositiveIntegerField(blank=True, null=True)
    ads_count_all = models.PositiveIntegerField(blank=True, null=True)
    is_collected = models.BooleanField(default=False)
    # TODO cards_count_average - add count of showing cards average by day

    class Meta:
        ordering = ['number_in_dict', ]

    def __str__(self):
        return self.word

    def _get_params(self):
        params = self.URL_PARAMS
        params['q'] = str(self.word)
        params['country'] = 'US'
        days_ago = 1
        params['start_date[min]'] = str(datetime.now().date() - timedelta(days=days_ago))
        return params

    def _prepare_url(self):
        prepare = PreparedRequest()
        prepare.prepare_url(self.FB_LIB_URL, self._get_params())
        return prepare.url

    @property
    def url(self):
        """Получить ссылку ads library с поиском по выбраному ключу"""
        return self._prepare_url()

    @staticmethod
    def get_bunch(length=20, k=2):
        if k < 1 or k >= 10:  # TODO set 10 as CONST
            raise ValueError('K must be more than 1 and less than 10')
        if length <= 0 or length >= 1000:
            raise ValueError('"count" must be more than zero or less than 1000')
        qs = KeyWord.objects.filter(number_in_dict__range=[(k-1)*1000 + 1, k*1000])\
                 .filter(is_collected=False).only('word')[:length]
        if not qs.exists():
            raise KeyWord.DoesNotExist # TODO
        to_update_words = [key.word for key in qs]
        KeyWord.objects.filter(word__in=to_update_words).update(is_collected=True)
        return qs

    @staticmethod
    def set_all_not_collected():
        KeyWord.objects.update(is_collected=False)



class MailService(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    pattern = models.CharField(max_length=30)
    examples = models.TextField(blank=True)
    ignore  = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class IgnoredMailGeo(models.Model):
    domain = models.CharField(max_length=3, primary_key=True)

    def __str__(self):
        return self.domain


class IgnoreGroupWord(models.Model):
    word = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.word

    def save(self, **kwargs):
        if not self.pk:
            self.word = self.word.lower()
        super().save(**kwargs)


class ActualGroupManager(models.Manager):
    def get_queryset(self):
        qs = FbGroup.objects.exclude(Q(email='') | Q(name='')).filter(last_ad_date=timezone.now().date())
        return qs


class NotCollectedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=FbGroup.NOT_LOADED)


class ErrorReqManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=FbGroup.ERROR_REQ)

class CollectedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=FbGroup.COLLECTED)


class NoDataManager(CollectedManager):
    def get_queryset(self):
        return super().get_queryset().filter(email='').filter(name='')


class NoMailManager(CollectedManager):
    def get_queryset(self):
        return super().get_queryset().filter(email='')


class FullDataManager(CollectedManager):
    def get_queryset(self):
        return super().get_queryset().exclude(Q(email='') | Q(name=''))


class FbGroup(models.Model):
    objects = models.Manager()
    not_collected_objects = NotCollectedManager()
    error_req_objects = ErrorReqManager()
    collected_objects = CollectedManager()
    collected_no_data_objects = NoDataManager()
    collected_no_mail_objects = NoMailManager()
    full_objects = FullDataManager()
    actual_objects = ActualGroupManager()

    FB_GROUP_PATTERN = 'http[s]?://facebook.com/..{0,100}'
    REQ_HTML_DIR = '/home/vlad/PycharmProjects/FbSearcher/fb/media/req_html_data'

    NOT_LOADED = 'not_loaded'
    NEED_LOGIN = 'need_login'
    ERROR_REQ = 'error_req'
    COLLECTED = 'collected'
    STATUSES = (
        (NOT_LOADED, 'Не загружен'),
        (NEED_LOGIN, 'Нужен вход'),
        (ERROR_REQ, 'Ошибка запроса'),
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
    email_service = models.ForeignKey(
        to=MailService,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    is_main_service_mark = models.BooleanField(default=False)
    is_ignore_word = models.BooleanField(blank=True, null=True)
    followers = models.CharField(
        max_length=50,
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
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return f'<FbGroup> {self.url}'

    @staticmethod
    def log_all_data():
        log_dir_path = 'fb_groups_logs'
        file_name = str(datetime.now().date()) + '.csv'
        file_path = os.path.join(settings.MEDIA_ROOT,log_dir_path, file_name)
        qs = FbGroup.full_objects.all()
        with open(file_path, 'w', newline='\n', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file, delimiter=',', quotechar='"')
            for group in qs:
                writer.writerow([group.pk,group.name, group.email])

    @property
    def url(self):
        if self.pk.isdigit():
            return f'https://www.facebook.com/profile.php?id={self.pk}'
        return f'https://facebook.com/{self.pk}/'

    @staticmethod
    def mark_mail_services():
        """Отметить какой email сервис"""
        mail_services = MailService.objects.all()
        # TODO make in transaction
        FbGroup.collected_objects.filter(email='').filter(is_main_service_mark=False).update(is_main_service_mark=True)
        groups = FbGroup.full_objects.only('email', 'email_service').filter(is_main_service_mark=False)
        for group in groups:
            for service in mail_services:
                if re.match('.+@' + service.pattern, group.email.lower()):
                    group.email_service = service
            group.is_main_service_mark = True
            group.save()

    @staticmethod
    def mark_ignored_name():
        """Пометить группы со стоп словами"""
        words = IgnoreGroupWord.objects.all()
        regex_words = ['.{0,255}' + word.word + '.{0,255}' for word in words]
        regex = '|'.join(regex_words)
        # TODO make in transaction
        FbGroup.collected_objects.update(is_ignore_word=False)
        groups = FbGroup.collected_objects.filter(name__iregex=regex)
        groups.update(is_ignore_word=True)


    @staticmethod
    def global_stat():
        print('All:', FbGroup.objects.count())
        print('Actual:', FbGroup.actual_objects.count())
        print('Full:', FbGroup.full_objects.count())
        print('Empty:', FbGroup.collected_no_data_objects.count())
        print('Not loaded:', FbGroup.not_collected_objects.count())

    @staticmethod
    def update_db_by_group_ids(ids: iter) -> dict:
        """Обновить базу групп со списка (айди групп)"""
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

    def update(self, data: dict):
        """Обновить группу из словаря"""
        self.name = data.get('name', self.name)
        self.email = data.get('email', self.email)
        self.title = data.get('title', self.title)
        self.followers = data.get('followers', self.followers)
        self.status = FbGroup.COLLECTED
        try:
            self.save()
        except OperationalError as error:
            print(error)
            print(self)
            print(data)

    def set_error_req(self):
        """Пометить группу ошибкой запроса"""
        self.status = self.ERROR_REQ
        self.save()

    def update_from_url(self, proxy, timeout=6, log=False):
        """Обновить данные по группе спарсив ссылку под прокси"""
        start = time.time()
        try:
            res = req.get(
                self.url,
                headers=headers,
                timeout=timeout,
                proxies={'https': proxy.url}
            )
            spend_time = res.elapsed.total_seconds()
        except (ConnectTimeout, ReadTimeout, ConnectionError, RequestException) as error:
            end = time.time()
            spend_time = end - start
            req_result = {
                'status': False,
                'error': error,
                'spend_time': spend_time,
            }
            self.status = self.ERROR_REQ
            self.save()

        else:
            if log:
                self.log_req_data(res.text)
            if res.status_code == 200:
                page = FbGroupPageNoAuth(res.text)
                page()
                parse_result = page.result
                self.update(parse_result)
                req_result = {
                    'status': True,
                    'result': parse_result,
                    'spend_time': spend_time,
                }
            else:
                req_result = {
                    'status': False,
                    'error': 'Status code not 200',
                    'spend_time': spend_time,
                }
        return req_result

    def log_req_data(self, html):
        """Залогировать полученый html от запроса"""
        if self.req_html_data:
            remove_if_exists(self.req_html_data.path)
        file = ContentFile(html)
        file_name = f'{self.pk}.html'
        self.req_html_data.save(file_name, file)

    @staticmethod
    def clean_all_data(qs=None):
        """Сбросить данные по группам"""
        if not qs:
            qs = FbGroup.objects.all()
            input('Are you whant to remove all? type y?n: ')
        qs.update(name='', email='', status=FbGroup.NOT_LOADED, req_html_data='', title='')
        if os.path.exists(FbGroup.REQ_HTML_DIR):
            shutil.rmtree(FbGroup.REQ_HTML_DIR)

    def set_not_loaded(self):
        """Сбросить данные по группе"""
        self.name = ''
        self.title = ''
        self.email = ''
        self.req_html_data = ''
        self.status = FbGroup.NOT_LOADED
        self.save()

    def mark_name(self):
        """Поменить группу маркером (для поиска в админ)"""
        self.name = 'xxx ' + self.name
        self.save()

    @staticmethod
    def create_file():
        # qs = FbGroup.full_objects.all()
        # path = './media/all.csv'
        # with open(path, 'w') as file:
        #     for group in qs:
        #         line = f'"{group.name}",{group.email}\n'
        #         file.write(line)
        #
        # return path
        qs = FbGroup.full_objects.all()[15000:20000]
        with open('/home/vlad/4.csv', 'w', newline='\n') as csv_file:
            writer = csv.writer(csv_file, delimiter=',', quotechar='"')
            # writer.writerow(['Some text and " dasd', 'email.com'])
            for group in qs:
                writer.writerow([group.name, group.email])
                group.is_used = True
                group.save()
        return '/home/vlad/all.csv'



class ThreadCounter(models.Model):
    name = models.CharField(max_length=20, primary_key=True)
    count = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    def stat(self):
        delta = self.last_update - self.created
        print(self,
              f'AVG: {round(int(self.count) / delta.total_seconds(), 1)}Count:{self.count} start:{self.created} last:{self.last_update}', )

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
