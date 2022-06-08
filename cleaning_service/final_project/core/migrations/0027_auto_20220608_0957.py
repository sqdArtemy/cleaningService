# Generated by Django 3.2.13 on 2022-06-08 04:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0026_auto_20220607_2222'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='profile_pic',
            new_name='picture',
        ),
        migrations.AlterField(
            model_name='review',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 8, 9, 57, 31, 196845), verbose_name='Time of creation'),
        ),
    ]
