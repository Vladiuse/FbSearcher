# Generated by Django 4.2.1 on 2024-01-29 21:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('countries', '0017_alter_countrycomment_type'),
        ('remote_pc', '0007_dsdailystat'),
    ]

    operations = [
        migrations.AddField(
            model_name='dsdailystat',
            name='country',
            field=models.ForeignKey(default='us', on_delete=django.db.models.deletion.CASCADE, to='countries.country'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dsdailystat',
            name='updated',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='dsdailystat',
            name='new',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='dsdailystat',
            name='total',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='dsdailystat',
            name='unique',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
