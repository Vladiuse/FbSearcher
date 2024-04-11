from django.db.models import Sum, Avg, Count, Max, F, FloatField
from django.db.models.functions import Round, Cast
from django.apps import apps
from django.db import models
from django.core.validators import RegexValidator

counter = 0


def get_pk():
    global counter
    counter += 1
    return counter


class WorldPart(models.Model):
    name = models.CharField(max_length=50)
    ru_name = models.CharField(max_length=50)
    color = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return self.ru_name


class Country(models.Model):
    iso = models.CharField(
        max_length=2,
        verbose_name='Код страны ISO',
        unique=True,
        primary_key=True,
    )
    iso3 = models.CharField(
        max_length=3,
        verbose_name='ISO 3',
        unique=True,
        blank=True,
        null=True,
    )
    ru_full_name = models.CharField(
        max_length=60,
        verbose_name='Русское название',
        blank=True,
        unique=True,
    )
    phone = models.CharField(
        max_length=15,
        verbose_name='Валидный номер',
        blank=True,
    )
    phone_code = models.CharField(
        max_length=15,
        verbose_name='Моб код страны',
        blank=True,
    )
    words = models.JSONField(
        default={"words": [], "templates": []},
        verbose_name='Слова под гео'
    )
    language = models.ManyToManyField(
        'Language',
        blank=True,
        through="CountryLanguage",
    )
    curr = models.ManyToManyField(
        'Currency',
        blank=True,
    )
    population = models.IntegerField(default=0)
    parse_population_conf = models.PositiveIntegerField(default=1, verbose_name='Коофициен для парса по населению')
    use_in_parse = models.BooleanField(default=False)
    world_part = models.ForeignKey(
        WorldPart,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='country'
    )

    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'

    def __str__(self):
        return self.pk.upper()

    def stat(self):
        if self.ds_stat.exists():
            stat = Country.objects.filter(pk=self.pk).aggregate(total_sum=Sum('ds_stat__total'),
                                                                unique_sum=Sum('ds_stat__unique'),
                                                                new_sum=Sum('ds_stat__new'))
            stat['unique_percent'] = round(stat['unique_sum'] / stat['total_sum'] * 100)
            stat['new_percent'] = round(stat['new_sum'] / stat['unique_sum'] * 100)
            return stat

    def country_new_daily_stat(self):
        """Статистика наработки по дням"""
        stat = self.ds_stat.values('created').annotate(new=Sum('new'), total=Sum('total')).annotate(
            avg=Cast(Round(F('new') / F('total') * 100, 1), FloatField())).order_by('created')
        return stat


class CountryComment(models.Model):
    TYPES = [
        ('danger', 'Danger'),
        ('primary', 'Primary'),
        ('success', 'Success'),
        ('warning', 'Warning'),
    ]
    country = models.ForeignKey(
        to=Country,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField()
    type = models.CharField(max_length=10, choices=TYPES, )
    created = models.DateField(auto_now_add=True)


class Language(models.Model):
    iso = models.CharField(
        max_length=2,
        verbose_name='Код iso языка',
        primary_key=True)
    russian_name = models.CharField(
        max_length=25,
        verbose_name='Русское название',
        blank=True
    )
    discount_text = models.CharField(max_length=250, blank=True)
    has_vocabulary = models.BooleanField(default=False)

    class Meta:
        ordering = ['iso']

    def __str__(self):
        return f'{self.russian_name}({self.iso.upper()})'


class Currency(models.Model):
    name = models.CharField(
        max_length=60,
        verbose_name='Название валюты'
    )
    iso = models.CharField(
        max_length=3,
        primary_key=True,
        verbose_name='Код валюты',
        unique=True)
    iso_3366 = models.CharField(
        max_length=3,
        verbose_name='ISO 3166-1',
        unique=True,
        blank=True,
        null=True
    )
    kma_code = models.CharField(
        max_length=5,
        verbose_name='Валюта в кма',
        blank=True,
        default=''
    )

    def __str__(self):
        return f'{self.name}({self.iso.upper()})'


class KeyWord(models.Model):
    number_in_dict = models.IntegerField()
    word = models.CharField(
        max_length=255,
        # validators=[RegexValidator(regex='([A-Za-z]){1,30}', message='Incorrect eng key word')]
    )
    language = models.ForeignKey(
        to=Language,
        on_delete=models.PROTECT,
        related_name='keywords',
    )

    class Meta:
        ordering = ['number_in_dict', ]
        # unique_together = ['word', 'language']

    def __str__(self):
        return f'{self.language_id} {self.number_in_dict}: {self.word}'


class CountryLanguage(models.Model):
    """Языковой словарь страны"""
    POP_KEYSDEEP_COOF = [
        # population, keys_deep
        [0, 200],
        [5, 300],
        [10, 500],
        [20, 1000],
        [40, 2000],
        [80, 2500],
        [120, 3500],
        [160, 4000],
        [200, 5000],
        [250, 7000],
        [300, 8000],
    ]

    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE,
                                related_name='vocabulary',
                                )
    keys_deep = models.PositiveIntegerField(blank=True, null=True, )
    weight = models.PositiveIntegerField(blank=True, default=1, verbose_name='Весовой кооф языковой группы')

    class Meta:
        verbose_name = 'Словарь по стране'
        verbose_name_plural = 'Словари по странам'
        unique_together = ['country', 'language']

    def __repr__(self):
        return f'CountryLang: {self.country_id}-{self.language_id}'

    def __str__(self):
        return f'{self.country_id}-{self.language_id}'.upper()

    @staticmethod
    def get_deep_by_pop(population):
        deep = None
        if not population:
            return deep
        for pop, keys_deep in CountryLanguage.POP_KEYSDEEP_COOF:
            if population >= pop:
                deep = keys_deep
        return deep

    def set_keys_deep(self):
        deep = CountryLanguage.get_deep_by_pop(self.speakers_population)
        self.keys_deep = deep
        self.save()

    @property
    def percent_of_lang(self) -> float:
        country = self.country
        vocs = country.vocabulary.all()
        total_weight = sum([voc.weight for voc in vocs])
        try:
            return round(self.weight / total_weight, 2)
        except ZeroDivisionError:
            return 0

    @property
    def speakers_population(self):
        return round(self.country.parse_population_conf * self.percent_of_lang)
