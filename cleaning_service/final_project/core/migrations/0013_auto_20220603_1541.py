# Generated by Django 3.2.13 on 2022-06-03 10:41

import datetime

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20220602_2246'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requeststatus',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('canceled', 'Canceled'), ('completed', 'Completed')], max_length=15, verbose_name='Request status'),
        ),
        migrations.AlterField(
            model_name='review',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 3, 15, 41, 28, 126417), verbose_name='Time of creation'),
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seen', models.BooleanField(default=False, verbose_name='Notification was seen')),
                ('header', models.CharField(max_length=156, verbose_name='Header of notification')),
                ('text', models.TextField(verbose_name='Text of the notification')),
                ('request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.request')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
