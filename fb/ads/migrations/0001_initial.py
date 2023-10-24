# Generated by Django 4.2.1 on 2023-09-25 18:19

import django.core.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FbGroup',
            fields=[
                ('group_id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=255)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('address', models.CharField(blank=True, max_length=255)),
                ('status', models.CharField(choices=[('not_loaded', 'Не загружен'), ('need_login', 'Нужен вход'), ('collected', 'Cобран')], default='not_loaded', max_length=15)),
                ('created', models.DateField(auto_now_add=True)),
                ('last_ad_date', models.DateField(default=django.utils.timezone.now)),
                ('req_html_data', models.FileField(blank=True, upload_to='req_html_data')),
            ],
        ),
        migrations.CreateModel(
            name='KeyWord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=30, unique=True, validators=[django.core.validators.RegexValidator(message='Incorrect eng key word', regex='([A-Za-z]){3,30}')])),
            ],
        ),
        migrations.CreateModel(
            name='ThreadCounter',
            fields=[
                ('name', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('count', models.IntegerField(default=0)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_update', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
