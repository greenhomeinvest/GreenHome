# Generated by Django 5.0.7 on 2024-10-02 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inquiry_message', '0004_imagesinquiry'),
    ]

    operations = [
        migrations.AddField(
            model_name='inquiry',
            name='city',
            field=models.CharField(blank=True, db_column='city', max_length=50, null=True),
        ),
    ]
