# Generated by Django 4.2.1 on 2023-10-19 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0016_ignoredmailgeo_ignoregroupword'),
    ]

    operations = [
        migrations.AddField(
            model_name='fbgroup',
            name='is_ignore_word_mark',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='fbgroup',
            name='is_main_service_mark',
            field=models.BooleanField(default=False),
        ),
    ]