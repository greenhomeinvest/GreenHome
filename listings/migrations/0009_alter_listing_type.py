# Generated by Django 5.0.7 on 2024-09-05 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0008_listing_toilet'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='type',
            field=models.CharField(choices=[('Мезонет', 'Mezonet'), ('Гараж', 'Garage'), ('Многостаен', 'Multyrooms'), ('Двустаен', '2 Rooms')], max_length=20),
        ),
    ]
