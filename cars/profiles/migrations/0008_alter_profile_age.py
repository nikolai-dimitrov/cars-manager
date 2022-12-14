# Generated by Django 4.1.3 on 2022-12-03 14:15

import cars.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0007_alter_profile_age_alter_profile_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='age',
            field=models.IntegerField(default=18, validators=[cars.core.validators.validate_age_gte_18]),
        ),
    ]
