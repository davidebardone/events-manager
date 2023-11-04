# Generated by Django 4.2.7 on 2023-11-04 15:41

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_alter_eventregistration_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='max_capacity',
            field=models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)]),
        ),
    ]
