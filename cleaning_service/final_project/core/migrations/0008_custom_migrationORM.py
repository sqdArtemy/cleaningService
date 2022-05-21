from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = ['core', '0001_initial']

    operations = [
        migrations.CreateModel(
            name='SampleMigrations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='id')),
                ('sample_field1', models.PositiveIntegerField(default=0, verbose_name='sample field 1')),
                ('sample_field2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.user')),
                ('sample_field3', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.request')),
            ],
        ),
    ]