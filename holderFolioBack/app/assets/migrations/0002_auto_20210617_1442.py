# Generated by Django 3.0.7 on 2021-06-17 12:42

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 17, 12, 42, 22, 996094, tzinfo=utc)),
        ),
    ]
