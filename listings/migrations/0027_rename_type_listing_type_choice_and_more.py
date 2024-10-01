# Generated by Django 5.0.7 on 2024-09-06 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0026_remove_listing_aditional_info_delete_aditionainfo'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='type',
            new_name='type_choice',
        ),
        migrations.RemoveField(
            model_name='moreoptions',
            name='listing',
        ),
        migrations.AddField(
            model_name='listing',
            name='more_options',
            field=models.ManyToManyField(blank=True, related_name='listings', to='listings.moreoptions'),
        ),
    ]
