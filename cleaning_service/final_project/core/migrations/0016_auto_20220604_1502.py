# Generated by Django 3.2.13 on 2022-06-04 10:02

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_auto_20220604_1411'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='rating',
            field=models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(0)], verbose_name='Star-rating'),
        ),
        migrations.AlterField(
            model_name='requeststatus',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('completed', 'Completed'), ('canceled', 'Canceled')], max_length=15, verbose_name='Request status'),
        ),
        migrations.AlterField(
            model_name='review',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 4, 15, 2, 46, 960716), verbose_name='Time of creation'),
        ),
        migrations.AlterField(
            model_name='review',
            name='rate',
            field=models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(0)], verbose_name='Star-rating'),
        ),
    ]
