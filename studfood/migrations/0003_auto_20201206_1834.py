# Generated by Django 3.1.3 on 2020-12-06 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studfood', '0002_foodmenu_details'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='foodmenu',
            name='picture',
        ),
        migrations.AddField(
            model_name='foodmenu',
            name='picture1',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
        migrations.AddField(
            model_name='foodmenu',
            name='picture2',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
