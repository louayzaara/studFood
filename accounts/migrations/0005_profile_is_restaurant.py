# Generated by Django 3.1.3 on 2020-12-08 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_profile_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='is_restaurant',
            field=models.BooleanField(default=False),
        ),
    ]
