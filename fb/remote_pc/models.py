from django.db import models
from django.db.models.functions import Concat
from django.utils import timezone
from django.db.models import Sum, Avg, Count, Max, F, FloatField
from django.db.models.functions import Round, Cast
from datetime import timedelta
from django.core.validators import RegexValidator
from countries.models import Country
from datetime import datetime


class DS(models.Model):
    PREFIXES = (
        ('PC', 'Желеска (PC)'),
        ('D', 'Дэдик (D)')
    )
    OS = (
        ('Windows', 'Windows'),
        ('Linux', 'Linux'),
    )
    WORK = 'Работает'
    NOT_WORK = 'Не работает'
    NOT_ACTIVE = 'Не активен'
    prefix = models.CharField(max_length=5, choices=PREFIXES, )
    number = models.CharField(max_length=50, )
    full_name = models.CharField(max_length=50, blank=True)
    ip = models.GenericIPAddressField()
    login = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    core = models.PositiveIntegerField()
    ram = models.PositiveIntegerField()
    os = models.CharField(max_length=50, choices=OS)
    last_activity = models.DateTimeField(blank=True, null=True)
    use_in_pars = models.BooleanField(default=True)
    color = models.CharField(max_length=7, blank=True, )

    def __str__(self):
        return self.name()

    class Meta:
        unique_together = ['prefix', 'number']
        verbose_name = 'DS'
        verbose_name_plural = 'DS'
        ordering = ['number', 'prefix']

    def name(self):
        return f'{self.prefix}{self.number}'

    def ping(self):
        self.last_activity = timezone.now()
        self.save()

    def past(self):
        if self.last_activity:
            delta = timezone.now() - self.last_activity
            return delta
        return ''

    @staticmethod
    def last_parse_date():
        return DSDailyStat.objects.aggregate(last_date=Max('created'))['last_date']

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
            if delta > timedelta(minutes=45):
                return NOT_ACTIVE
            elif delta > timedelta(minutes=10):
                return NOT_WORK
            elif delta > timedelta(minutes=5):
                return MAYBE_WORK
            else:
                return WORK
        return NOT_ACTIVE

    @staticmethod
    def daily_total_stat():
        return DSDailyStat.objects.values('created').annotate(total=Sum('total')).order_by('created')

    @staticmethod
    def dss_today_stat():
        last_date = DS.last_parse_date()
        stat = DSDailyStat.objects.select_related('ds').filter(created=last_date).values('ds', 'ds__number',
                                                                                         'ds__prefix',
                                                                                         'ds__color', ).annotate(
            avg=Sum('total') / Count('created', distinct=True)
        )
        return sorted(stat, key=lambda item: (item['ds__prefix'], int(item['ds__number'])))

    @staticmethod
    def dss_avg_stat():
        stat = DSDailyStat.objects.select_related('ds').values('ds', 'ds__number', 'ds__prefix',
                                                               'ds__color', ).annotate(
            avg=Sum('total') / Count('created', distinct=True)
        )
        return sorted(stat, key=lambda item: (item['ds__prefix'], int(item['ds__number'])))


class DSDailyStat(models.Model):
    ds = models.ForeignKey(DS, on_delete=models.CASCADE)
    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        related_name='ds_stat',
    )
    total = models.PositiveIntegerField(default=0)
    unique = models.PositiveIntegerField(default=0)
    new = models.PositiveIntegerField(default=0)
    updated = models.PositiveIntegerField(default=0)
    created = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ['ds', 'created', 'country']

    @staticmethod
    def country_last_date_new_stat():
        """статистика новых за последний день по странам"""
        last_date = DS.last_parse_date()
        stat = (DSDailyStat.objects.filter(created=last_date).values('country_id').
                annotate(new=Sum('new'), total=Sum('total')).
                annotate(avg=Cast(Round(F('new') / F('total') * 100, 1), FloatField())
                         ))
        stat = sorted(stat, key=lambda item: item['avg'], reverse=True)  # TODO rename avg
        return {
            'date': last_date,
            'stat': stat,
        }

    @staticmethod
    def add_parse_stat(ds_name, country_code, data):
        date = datetime.now().date()
        ds = DS.objects.annotate(namedb=Concat('prefix', 'number')).get(namedb=ds_name)
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

    @staticmethod
    def total_new_stat():
        pass
        stat = DSDailyStat.objects.values('created').annotate(total=Sum('total'), new=Sum('new')).order_by('created')
        for item in stat:
            # item['new'] = int(item['new'] / 1000)
            # item['total'] = int(item['total'] / 1000)
            try:
                item['percent'] = round(item['new'] / item['total'] * 100,2)
            except ZeroDivisionError:
                item['percent'] = 0
        for i in stat:
            print(i)
        return stat

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
