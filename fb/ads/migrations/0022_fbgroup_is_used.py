# Generated by Django 4.2.1 on 2023-10-24 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0021_alter_keyword_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='fbgroup',
            name='is_used',
            field=models.BooleanField(default=False),
        ),
    ]