# Generated by Django 4.2.1 on 2023-10-19 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0018_remove_fbgroup_is_ignore_word_mark_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='keyword',
            name='number_in_dict',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='keyword',
            name='ru_word',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
