# Generated by Django 4.2.1 on 2023-12-19 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('remote_pc', '0004_settings'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ds',
            options={'ordering': ['name'], 'verbose_name': 'DS', 'verbose_name_plural': 'DS'},
        ),
        migrations.AddField(
            model_name='ds',
            name='full_name',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]