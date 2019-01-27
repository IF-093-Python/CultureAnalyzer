# Generated by Django 2.1.5 on 2019-01-26 13:26

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('indicators', '0002_auto_20190126_0004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='countryindicator',
            name='PDI',
            field=models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(100)]),
        ),
    ]