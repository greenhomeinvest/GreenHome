# Generated by Django 5.0.7 on 2024-08-27 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inquiry_message', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='inquiry',
            name='type_property',
            field=models.CharField(choices=[('3-bed', '3-стаен'), ('2-bed', '2-стаен'), ('maisonette', 'Мезонет'), ('garage', 'Гараж'), ('shop', 'Магазин')], db_column='type_property', default='Вид имот', max_length=20),
        ),
    ]
