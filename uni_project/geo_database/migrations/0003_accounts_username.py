# Generated by Django 3.2 on 2021-04-25 02:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geo_database', '0002_alter_accounts_account_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='accounts',
            name='username',
            field=models.CharField(default='random_user', max_length=50),
        ),
    ]