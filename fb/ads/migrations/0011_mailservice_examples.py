# Generated by Django 4.2.1 on 2023-10-12 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0010_fbgroup_email_service'),
    ]

    operations = [
        migrations.AddField(
            model_name='mailservice',
            name='examples',
            field=models.TextField(blank=True),
        ),
    ]
