# Generated by Django 3.0.7 on 2021-06-19 16:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0007_auto_20210618_1443'),
        ('exchange', '0005_auto_20210618_2320'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exchange',
            name='portfolio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='portfolio', to='portfolio.PortFolio'),
        ),
    ]
