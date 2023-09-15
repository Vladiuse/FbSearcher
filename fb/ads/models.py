from django.db import models

def clean_fb_group_url(url):
    pass



class FbGroup(models.Model):

    GROUP_DOMAIN = 'facebook.com'

    id = models.CharField(
        max_length=255,
        primary_key=True,)
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
    raw_url = models.URLField()


class FbLibAd(models.Model):
    AD_STATUS = (
        ('1', 'Активна'),
        ('0', 'Не активна'),
    )
    group = models.ForeignKey(
        to=FbGroup,
        on_delete=models.CASCADE,
        related_name='ads',
    )
    id = models.BigIntegerField(
        primary_key=True,
    )
    time_text = models.CharField(
        max_length=255,
    )
    status = models.CharField(
        max_length=1,
        choices=AD_STATUS,
    )
    created = models.DateTimeField(
        auto_now_add=True,
    )

