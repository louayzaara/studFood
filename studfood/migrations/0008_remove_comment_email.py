# Generated by Django 3.1.3 on 2020-12-07 17:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('studfood', '0007_auto_20201207_1736'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='email',
        ),
    ]
