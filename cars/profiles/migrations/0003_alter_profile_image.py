# Generated by Django 4.1.3 on 2022-11-29 20:01

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=cloudinary.models.CloudinaryField(default='https://res.cloudinary.com/dltjy2gzz/image/upload/v1669752042/profiles/default/profile_qmzvir.jpg', max_length=255, verbose_name='Image'),
        ),
    ]