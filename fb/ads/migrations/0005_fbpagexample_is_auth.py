# Generated by Django 4.2.1 on 2023-09-29 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0004_fbpagexample_orig_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='fbpagexample',
            name='is_auth',
            field=models.BooleanField(default=0, verbose_name='Выполнен ли вход'),
            preserve_default=False,
        ),
    ]