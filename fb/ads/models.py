from django.db import models
from urllib.parse import urlparse
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
import re
from django.utils import timezone


class FbGroup(models.Model):
    FB_GROUP_PATTERN = 'http[s]?://facebook.com/..{0,100}'

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
    # url = models.URLField(
    #     validators=[RegexValidator(regex=r'http[s]?://facebook.com/..{0,100}'),],
    #     unique=True,
    # )
    created = models.DateField(
        auto_now_add=True,
    )
    last_ad_date = models.DateField(default=timezone.now)

    @staticmethod
    def fb_group_url_to_id(url):
        url = urlparse(url).path
        if url.startswith('/'):
            url = url[1:]
        if url.endswith('/'):
            url = url[:-1]
        return url

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
