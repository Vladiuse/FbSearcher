# Generated by Django 4.2.1 on 2023-10-09 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proxies', '0004_proxy_proxy_ip_proxyauth_proxy_ip_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='proxy',
            name='error_text',
        ),
        migrations.RemoveField(
            model_name='proxyauth',
            name='error_text',
        ),
        migrations.RemoveField(
            model_name='proxymobile',
            name='error_text',
        ),
        migrations.AddField(
            model_name='proxy',
            name='error_text_full',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='proxy',
            name='error_type',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='proxyauth',
            name='error_text_full',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='proxyauth',
            name='error_type',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='proxymobile',
            name='error_text_full',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='proxymobile',
            name='error_type',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
