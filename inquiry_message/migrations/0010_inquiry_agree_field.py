# Generated by Django 5.0.7 on 2024-10-06 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inquiry_message', '0009_remove_inquiry_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='inquiry',
            name='agree_field',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
