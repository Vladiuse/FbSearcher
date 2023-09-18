import os.path

from django.db import models
from urllib.parse import urlparse
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
import re
from django.utils import timezone
from .fb_group_page import FbGroupPage
import requests as req
from django.core.files.base import ContentFile
from io import StringIO
from django.db.models import Q
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5'
}

class KeyWord(models.Model):
    word = models.CharField(
        max_length=30,
        unique=True,
        validators=[RegexValidator(regex='([A-Za-z]){3,30}', message='Incorrect eng key word')])

    def __str__(self):
        return self.word


class FullFbGroupManager(models.Manager):

    def get_queryset(self):
        qs = FbGroup.objects.exclude(Q(email='') |Q(name=''))
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

    FB_GROUP_PATTERN = 'http[s]?://facebook.com/..{0,100}'

    NOT_LOADED = 'not_loaded'
    NEED_LOGIN = 'not_loaded'
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

    @staticmethod
    def fb_group_url_to_id(url):
        url = urlparse(url).path
        if url.startswith('/'):
            url = url[1:]
        if url.endswith('/'):
            url = url[:-1]
        return url

    @property
    def url(self):
        return f'https://facebook.com/{self.pk}/'

    def get_group_req_html(self, log_html_data=False) ->str:
        """Получить исходный код страницы группы"""
        res = req.get(self.url, headers=headers)
        if res.status_code == 200:
            if log_html_data:
                self.log_html_source_file(html=res.text)
            return res.text
        else:
            print('Error req', res.status_code, self)
            return ''

    def log_html_source_file(self, html):
        if os.path.exists(self.req_html_data.path):
            os.remove(self.req_html_data.path)
        file = ContentFile(html)
        self.req_html_data.save(f'{self.pk}.html', file)

    def update_group_info(self):
        html = self.get_group_req_html()
        if html:
            page = FbGroupPage(html)

            if page.is_login_form:
                self.status = self.NEED_LOGIN
            else:
                page()
                self.email = page.result.pop('group_email', self.email)
                self.name = page.result.pop('group_name', self.name)
                self.save()
                self.status = self.COLLECTED

    # def get_page_data(self):
    #     try:
    #         with open(self.req_html_data.path) as file:
    #             html = file.read()
    #         page = FbGroupPage(html)
    #         page()
    #         print(page.result)
    #         self.email = page.result.pop('group_email', self.email)
    #         self.name = page.result.pop('group_name', self.name)
    #         self.save()
    #     except Exception as error:
    #         print(error)

    # @staticmethod
    # def create_from_url():
#
# class FbLibAd(models.Model):
#     ACTIVE = 'Активно'
#     NOT_ACTIVE = 'Не активно'
#
#     ACTIVE_CODE = '1'
#     NOT_ACTIVE_CODE = '0'
#     AD_STATUS = (
#         (ACTIVE_CODE, ACTIVE),
#         (NOT_ACTIVE_CODE, NOT_ACTIVE),
#     )
#     group = models.ForeignKey(
#         to=FbGroup,
#         on_delete=models.CASCADE,
#         related_name='ads',
#     )
#     id = models.BigIntegerField(
#         primary_key=True,
#     )
#     time_text = models.CharField(
#         max_length=255,
#     )
#     status = models.CharField(
#         max_length=1,
#         choices=AD_STATUS,
#     )
#     last_update = models.DateTimeField(
#         auto_now=True,
#     )
#     created = models.DateTimeField(
#         auto_now_add=True,
#     )
#
#
#     @staticmethod
#     def create_or_update(*, group, id, **kwargs):
#         try:
#             ad = FbLibAd.objects.get(group=group, id=id)
#             created = False
#             # update
#             ad.status = kwargs.get('status', ad.status)
#             ad.time_text = kwargs.get('time_text', ad.time_text)
#             ad.full_clean()
#             ad.save()
#         except FbLibAd.DoesNotExist:
#             ad = FbLibAd(group=group, id=id,  **kwargs)
#             ad.full_clean()
#             ad.save()
#             created = True
#         return ad, created
