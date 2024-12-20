# Generated by Django 3.2.13 on 2022-06-05 15:18

import datetime

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_auto_20220604_2333'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='service',
            name='cost',
        ),
        migrations.AddField(
            model_name='service',
            name='description',
            field=models.TextField(default=1, verbose_name='Description of a service'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='service',
            name='hours_required',
            field=models.FloatField(default=1, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Hours required to complete this service'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='hour_cost',
            field=models.FloatField(default=1, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Cost per working hour'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='notification',
            name='request',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Request', to='core.request'),
        ),
        migrations.AlterField(
            model_name='request',
            name='total_cost',
            field=models.FloatField(default=0, verbose_name='Final cost of the service'),
        ),
        migrations.AlterField(
            model_name='requeststatus',
            name='status',
            field=models.CharField(choices=[('canceled', 'Canceled'), ('pending', 'Pending'), ('completed', 'Completed'), ('accepted', 'Accepted')], max_length=15, verbose_name='Request status'),
        ),
        migrations.AlterField(
            model_name='review',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 5, 20, 18, 13, 106062), verbose_name='Time of creation'),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_cost', models.FloatField(default=0, verbose_name='Total cost of the order')),
                ('accepted', models.BooleanField(default=False, verbose_name='Is order accepted by user')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Company_order', to=settings.AUTH_USER_MODEL)),
                ('notification', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.notification')),
                ('request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Request_order', to='core.request')),
            ],
        ),
    ]
