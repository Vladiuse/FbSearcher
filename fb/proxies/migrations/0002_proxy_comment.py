# Generated by Django 4.2.1 on 2023-09-26 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proxies', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='proxy',
            name='comment',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]