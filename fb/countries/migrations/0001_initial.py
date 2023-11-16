# Generated by Django 4.2.1 on 2023-10-27 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('name', models.CharField(max_length=60, verbose_name='Название валюты')),
                ('iso', models.CharField(max_length=3, primary_key=True, serialize=False, unique=True, verbose_name='Код валюты')),
                ('iso_3366', models.CharField(blank=True, max_length=3, null=True, unique=True, verbose_name='ISO 3166-1')),
                ('kma_code', models.CharField(blank=True, default='', max_length=5, verbose_name='Валюта в кма')),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('iso', models.CharField(max_length=2, primary_key=True, serialize=False, verbose_name='Код iso языка')),
                ('russian_name', models.CharField(blank=True, max_length=25, verbose_name='Русское название')),
                ('discount_text', models.CharField(blank=True, max_length=250)),
            ],
            options={
                'ordering': ['iso'],
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('iso', models.CharField(max_length=2, primary_key=True, serialize=False, unique=True, verbose_name='Код страны ISO')),
                ('iso3', models.CharField(blank=True, max_length=3, null=True, unique=True, verbose_name='ISO 3')),
                ('ru_full_name', models.CharField(blank=True, max_length=60, unique=True, verbose_name='Русское название')),
                ('phone', models.CharField(blank=True, max_length=15, verbose_name='Валидный номер')),
                ('phone_code', models.CharField(blank=True, max_length=15, verbose_name='Моб код страны')),
                ('words', models.JSONField(default={'templates': [], 'words': []}, verbose_name='Слова под гео')),
                ('curr', models.ManyToManyField(blank=True, to='countries.currency')),
                ('language', models.ManyToManyField(blank=True, to='countries.language')),
            ],
            options={
                'verbose_name': 'Страна',
                'verbose_name_plural': 'Страны',
            },
        ),
    ]