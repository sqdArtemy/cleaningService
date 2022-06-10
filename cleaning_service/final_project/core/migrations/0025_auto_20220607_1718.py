# Generated by Django 3.2.13 on 2022-06-07 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0024_auto_20220606_2217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requeststatus',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('in_progress', 'In progress'), ('completed', 'Completed'), ('canceled', 'Canceled')], max_length=15, verbose_name='Request status'),
        ),
        migrations.AlterField(
            model_name='review',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Time of creation'),
        ),
    ]