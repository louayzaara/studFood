# Generated by Django 3.1.3 on 2020-12-06 20:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('studfood', '0004_foodmenu_picture3'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foodmenu',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
