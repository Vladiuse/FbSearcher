# Generated by Django 4.2.1 on 2023-10-12 17:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0009_remove_mailservice_id_alter_fbgroup_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='fbgroup',
            name='email_service',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ads.mailservice'),
        ),
    ]
