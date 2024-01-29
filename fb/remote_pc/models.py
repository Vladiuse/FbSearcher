from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.core.validators import RegexValidator
from countries.models import Country
from datetime import datetime

class DS(models.Model):
    OS = (
        ('Windows', 'Windows'),
        ('Linux', 'Linux'),
    )
    WORK = 'Работает'
    NOT_WORK = 'Не работает'
    NOT_ACTIVE = 'Не активен'
    name = models.CharField(max_length=50, blank=True, unique=True)
    full_name = models.CharField(max_length=50, blank=True)
    ip = models.GenericIPAddressField()
    login = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    core = models.PositiveIntegerField()
    ram = models.PositiveIntegerField()
    os = models.CharField(max_length=50,choices=OS)
    last_activity = models.DateTimeField(blank=True, null=True)
    use_in_pars = models.BooleanField(default=True)

    def __str__(self):
        return f'<{self.name}> {self.ip} {self.full_name}'

    class Meta:
        verbose_name = 'DS'
        verbose_name_plural = 'DS'
        ordering = ['name']

    def ping(self):
        self.last_activity = timezone.now()
        self.save()

    def past(self):
        if self.last_activity:
            delta = timezone.now() - self.last_activity
            return delta
        return ''

    @property
    def status(self):
        WORK = {
            'text': DS.WORK,
            'color': 'success',
        }
        MAYBE_WORK = {
            'text': DS.WORK,
            'color': 'warning',
        }
        NOT_WORK = {
            'text': DS.NOT_WORK,
            'color': 'danger',
        }
        NOT_ACTIVE = {
            'text': DS.NOT_ACTIVE,
            'color': 'secondary',
        }
        if self.last_activity:
            delta = timezone.now() - self.last_activity
            if delta >  timedelta(minutes=45):
                return NOT_ACTIVE
            elif delta > timedelta(minutes=10):
                return NOT_WORK
            elif delta > timedelta(minutes=5):
                return MAYBE_WORK
            else:
                return WORK
        return NOT_ACTIVE


class DSDailyStat(models.Model):
    ds = models.ForeignKey(DS, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    total = models.PositiveIntegerField(default=0)
    unique = models.PositiveIntegerField(default=0)
    new = models.PositiveIntegerField(default=0)
    updated = models.PositiveIntegerField(default=0)
    created = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ['ds', 'created']

    @staticmethod
    def add_parse_stat(ds_name, country_code, data):
        date = datetime.now().date()
        ds = DS.objects.get(name=ds_name)
        country = Country.objects.get(pk=country_code)
        ds_daily_stat_record, created = DSDailyStat.objects.get_or_create(
            created=date,
            country=country,
            ds=ds,
        )
        ds_daily_stat_record.total = ds_daily_stat_record.total + data['total']
        ds_daily_stat_record.unique = ds_daily_stat_record.unique + data['unique']
        ds_daily_stat_record.updated = ds_daily_stat_record.updated + data['updated']
        ds_daily_stat_record.new = ds_daily_stat_record.new + data['new']
        ds_daily_stat_record.save()


class Settings(models.Model):
    name = models.CharField(
        primary_key=True,
        max_length=50,
        validators=[RegexValidator(regex='^[a-zA-Z_]+$')],
    )
    desc = models.CharField(max_length=255, blank=True)
    value = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Settings'
        verbose_name_plural = 'Settings'

    def __str__(self):
        return self.name