# Generated by Django 5.0.7 on 2024-09-16 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0034_remove_listing_more_options_delete_moreoptions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='side_view',
            field=models.CharField(blank=True, choices=[('Западно изложение', 'Западно изложение'), ('Южно изложение', 'Южно изложение'), ('Северно изложение', 'Северно изложение'), ('Североизточното изложение', 'Североизточното изложение'), ('Северозападното изложение', 'Северозападното изложение'), ('Югозапад изложение', 'Югозапад изложение')], max_length=50, null=True),
        ),
    ]
