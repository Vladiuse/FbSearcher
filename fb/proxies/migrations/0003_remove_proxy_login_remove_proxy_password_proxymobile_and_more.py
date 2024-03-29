# Generated by Django 4.2.1 on 2023-10-02 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proxies', '0002_proxy_comment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='proxy',
            name='login',
        ),
        migrations.RemoveField(
            model_name='proxy',
            name='password',
        ),
        migrations.CreateModel(
            name='ProxyMobile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.GenericIPAddressField()),
                ('port', models.CharField(max_length=6)),
                ('status', models.BooleanField(default=None, max_length=50, null=True)),
                ('error_text', models.CharField(blank=True, max_length=255)),
                ('protocol', models.CharField(choices=[('http', 'http'), ('https', 'https'), ('socks5', 'socks5')], default='http', max_length=10)),
                ('created', models.DateField(auto_now_add=True)),
                ('comment', models.CharField(blank=True, max_length=255)),
                ('login', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=30)),
                ('change_ip_url', models.URLField()),
            ],
            options={
                'abstract': False,
                'unique_together': {('ip', 'port')},
            },
        ),
        migrations.CreateModel(
            name='ProxyAuth',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.GenericIPAddressField()),
                ('port', models.CharField(max_length=6)),
                ('status', models.BooleanField(default=None, max_length=50, null=True)),
                ('error_text', models.CharField(blank=True, max_length=255)),
                ('protocol', models.CharField(choices=[('http', 'http'), ('https', 'https'), ('socks5', 'socks5')], default='http', max_length=10)),
                ('created', models.DateField(auto_now_add=True)),
                ('comment', models.CharField(blank=True, max_length=255)),
                ('login', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=30)),
            ],
            options={
                'abstract': False,
                'unique_together': {('ip', 'port')},
            },
        ),
    ]
