# Generated by Django 3.2.13 on 2022-06-04 11:56

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_auto_20220604_1502'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Company', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='requeststatus',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('canceled', 'Canceled'), ('completed', 'Completed')], max_length=15, verbose_name='Request status'),
        ),
        migrations.AlterField(
            model_name='review',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 4, 16, 56, 41, 638483), verbose_name='Time of creation'),
        ),
    ]