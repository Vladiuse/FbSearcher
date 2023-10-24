# Generated by Django 4.2.1 on 2023-10-13 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0012_keyword_ads_count'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='keyword',
            options={'ordering': ['-ads_count']},
        ),
        migrations.AlterField(
            model_name='keyword',
            name='ads_count',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]