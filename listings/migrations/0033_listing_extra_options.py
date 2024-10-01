# Generated by Django 5.0.7 on 2024-09-16 06:58

import multiselectfield.db.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0032_alter_photos_listing'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='extra_options',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('Гараж', 'Гараж'), ('Басейн', 'Басейн'), ('Паркинг', 'Паркинг'), ('Градина', 'Градина'), ('В строеж', 'В строеж'), ('С преход', 'С преход'), ('Асансьор', 'Асансьор')], default=1, max_length=55),
            preserve_default=False,
        ),
    ]
