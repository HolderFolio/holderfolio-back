# Generated by Django 3.0.7 on 2021-06-21 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0007_auto_20210618_1415'),
    ]

    operations = [
        migrations.AddField(
            model_name='asset',
            name='name',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
