# Generated by Django 4.0.4 on 2022-05-06 10:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('naming', models.CharField(max_length=100, verbose_name='Category name')),
            ],
        ),
        migrations.AlterField(
            model_name='userrole',
            name='role',
            field=models.CharField(choices=[('company', 'Company'), ('customer', 'Customer')], max_length=15, verbose_name='User`s role'),
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Service name')),
                ('cost', models.FloatField(default=0, verbose_name='Cost of service per m^2')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.category')),
            ],
        ),
    ]