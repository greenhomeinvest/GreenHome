# Generated by Django 5.0.7 on 2024-07-17 07:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='listing',
            options={'verbose_name': 'Property Listing', 'verbose_name_plural': 'Property Listings'},
        ),
        migrations.AlterModelOptions(
            name='photos',
            options={'verbose_name': 'Property Photo', 'verbose_name_plural': 'Property Photos'},
        ),
    ]
