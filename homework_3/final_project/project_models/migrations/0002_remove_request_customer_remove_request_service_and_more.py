# Generated by Django 4.0.4 on 2022-05-05 11:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project_models', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='request',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='request',
            name='service',
        ),
        migrations.RemoveField(
            model_name='request',
            name='status',
        ),
        migrations.RemoveField(
            model_name='review',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='review',
            name='request',
        ),
        migrations.RemoveField(
            model_name='service',
            name='category',
        ),
        migrations.RemoveField(
            model_name='user',
            name='role',
        ),
        migrations.DeleteModel(
            name='Category',
        ),
        migrations.DeleteModel(
            name='Request',
        ),
        migrations.DeleteModel(
            name='RequestStatus',
        ),
        migrations.DeleteModel(
            name='Review',
        ),
        migrations.DeleteModel(
            name='Service',
        ),
        migrations.DeleteModel(
            name='User',
        ),
        migrations.DeleteModel(
            name='UserRole',
        ),
    ]
