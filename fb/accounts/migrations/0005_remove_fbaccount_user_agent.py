# Generated by Django 4.2.1 on 2023-09-28 16:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_fbaccount_user_agent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fbaccount',
            name='user_agent',
        ),
    ]
