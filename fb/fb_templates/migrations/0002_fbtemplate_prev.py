# Generated by Django 4.2.1 on 2023-10-20 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fb_templates', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='fbtemplate',
            name='prev',
            field=models.URLField(blank=True),
        ),
    ]
