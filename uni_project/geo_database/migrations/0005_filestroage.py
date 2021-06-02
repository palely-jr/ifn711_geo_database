# Generated by Django 3.0.5 on 2021-06-01 08:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('geo_database', '0004_auto_20210504_1909'),
    ]

    operations = [
        migrations.CreateModel(
            name='fileStroage',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('total_file_size', models.CharField(max_length=200)),
                ('used_file_size', models.CharField(max_length=200)),
                ('remaining_file_size', models.CharField(max_length=200)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'file_storage',
            },
        ),
    ]