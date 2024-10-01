# Generated by Django 5.0.7 on 2024-09-05 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0018_alter_listing_year_of_construction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moreoptions',
            name='name',
            field=models.CharField(blank=True, choices=[('Гараж', 'Гараж'), ('Басейн', 'Басейн'), ('Паркинг', 'Паркинг'), ('Градина', 'Градина'), ('В строеж', 'В строеж'), ('С преход', 'С преход'), ('Асансьор', 'Асансьор')], max_length=20, null=True, unique=True),
        ),
    ]
