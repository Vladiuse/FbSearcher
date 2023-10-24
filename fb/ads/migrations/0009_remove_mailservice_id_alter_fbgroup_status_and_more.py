# Generated by Django 4.2.1 on 2023-10-12 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0008_fbgroup_followers'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mailservice',
            name='id',
        ),
        migrations.AlterField(
            model_name='fbgroup',
            name='status',
            field=models.CharField(choices=[('not_loaded', 'Не загружен'), ('need_login', 'Нужен вход'), ('error_req', 'Ошибка запроса'), ('collected', 'Cобран')], default='not_loaded', max_length=15),
        ),
        migrations.AlterField(
            model_name='mailservice',
            name='name',
            field=models.CharField(max_length=50, primary_key=True, serialize=False),
        ),
    ]
