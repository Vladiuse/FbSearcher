# Generated by Django 4.2.1 on 2023-10-13 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0011_mailservice_examples'),
    ]

    operations = [
        migrations.AddField(
            model_name='keyword',
            name='ads_count',
            field=models.PositiveIntegerField(blank=True, default=0),
            preserve_default=False,
        ),
    ]