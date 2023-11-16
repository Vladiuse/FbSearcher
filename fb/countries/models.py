from django.db import models
from django.core.validators import RegexValidator

# Create your models here.
counter = 0
def get_pk():
    global counter
    counter += 1
    return counter



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
    )
    curr = models.ManyToManyField(
        'Currency',
        blank=True,
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
        max_length=255,
        #validators=[RegexValidator(regex='([A-Za-z]){1,30}', message='Incorrect eng key word')]
    )
    language = models.ForeignKey(
        to=Language,
        on_delete=models.PROTECT,
    )
    # TODO cards_count_average - add count of showing cards average by day

    class Meta:
        ordering = ['number_in_dict', ]
        # unique_together = ['word', 'language']

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

