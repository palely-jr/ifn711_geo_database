# Generated by Django 3.0.5 on 2021-06-07 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geo_database', '0002_auto_20210607_1720'),
    ]

    operations = [
        migrations.AddField(
            model_name='filestorage',
            name='company_name',
            field=models.CharField(default='', max_length=200),
        ),
    ]