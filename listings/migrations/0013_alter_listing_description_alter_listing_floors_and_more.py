# Generated by Django 5.0.7 on 2024-09-05 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0012_alter_moreoptions_options_alter_moreoptions_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='listing',
            name='floors',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='listing',
            name='floors_max',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='listing',
            name='more',
            field=models.ManyToManyField(blank=True, null=True, to='listings.option'),
        ),
    ]
