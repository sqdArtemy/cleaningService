# Generated by Django 4.0.4 on 2022-05-05 10:57

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('naming', models.CharField(max_length=100, verbose_name='Category name')),
            ],
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_area', models.FloatField(default=0, verbose_name='Total area to be cleaned')),
                ('address', models.TimeField(verbose_name='User`s address')),
                ('total_cost', models.FloatField(verbose_name='Final cost of the service')),
            ],
        ),
        migrations.CreateModel(
            name='RequestStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('completed', 'Completed'), ('canceled', 'Canceled'), ('pending', 'Pending')], max_length=15, verbose_name='Request status')),
            ],
        ),
        migrations.CreateModel(
            name='UserRole',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('customer', 'Customer'), ('company', 'Company')], max_length=15, verbose_name='User`s role')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='User`s name')),
                ('email', models.EmailField(max_length=254, verbose_name='User`s email')),
                ('phone', models.CharField(max_length=100, verbose_name='User`s phone')),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project_models.userrole')),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Service name')),
                ('cost', models.FloatField(default=0, verbose_name='Cost of service per m^2')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project_models.category')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feedback', models.TimeField(verbose_name='Customer`s feedback')),
                ('rate', models.PositiveIntegerField(default=0, verbose_name='Star-rating')),
                ('created_at', models.DateTimeField(default=datetime.datetime(2022, 5, 5, 15, 57, 20, 711541), verbose_name='Time of creation')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project_models.user')),
                ('request', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='project_models.request')),
            ],
        ),
        migrations.AddField(
            model_name='request',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project_models.user'),
        ),
        migrations.AddField(
            model_name='request',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project_models.service'),
        ),
        migrations.AddField(
            model_name='request',
            name='status',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='project_models.requeststatus'),
        ),
    ]
