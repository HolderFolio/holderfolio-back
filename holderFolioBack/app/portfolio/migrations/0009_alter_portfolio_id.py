# Generated by Django 3.2.4 on 2021-06-22 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0008_auto_20210619_1833'),
    ]

    operations = [
        migrations.AlterField(
            model_name='portfolio',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
