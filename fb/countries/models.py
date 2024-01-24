from django.db import models
from django.core.validators import RegexValidator

# Create your models here.
counter = 0


def get_pk():
    global counter
    counter += 1
    return counter

class WorldPart(models.Model):
    name = models.CharField(max_length=50)
    ru_name = models.CharField(max_length=50)

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
    use_in_parse = models.BooleanField(default=False)
    world_part = models.ForeignKey(
        WorldPart,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'

    def __str__(self):
        return self.pk.upper()


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
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE,
                                related_name='vocabulary',
                                )
    keys_deep = models.PositiveIntegerField(blank=True, null=True, )

