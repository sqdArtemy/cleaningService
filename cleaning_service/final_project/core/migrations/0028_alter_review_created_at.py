# Generated by Django 3.2.13 on 2022-06-08 12:04

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0027_auto_20220608_0957'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 8, 12, 4, 33, 697185, tzinfo=utc), verbose_name='Time of creation'),
        ),
    ]