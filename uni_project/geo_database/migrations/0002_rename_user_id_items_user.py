# Generated by Django 3.2 on 2021-05-04 08:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('geo_database', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='items',
            old_name='user_id',
            new_name='user',
        ),
    ]
