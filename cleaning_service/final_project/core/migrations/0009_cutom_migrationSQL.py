from django.db import migrations, models
import django.db.models.deletion


class Migrations(migrations.Migration):

    dependencies = ['core', '0001_initial']

    operations = [
        migrations.RunSQL(
            'CREATE TABLE IF NOT EXISTS "sample_model" ( "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,'
            '"sample_field" varchar(250) NOT NULL, "sample_field2" varchar(150) NOT NULL, "sample_field3"'
            'integer NOT NULL, "sample_field4" datetime NOT NULL'
            ')'

        )
    ]