# Generated by Django 3.1.3 on 2020-12-07 17:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('studfood', '0006_comment'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['created_at'], 'verbose_name_plural': 'Comments'},
        ),
    ]