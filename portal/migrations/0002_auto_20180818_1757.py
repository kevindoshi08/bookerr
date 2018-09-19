# Generated by Django 2.1 on 2018-08-18 12:27

from django.db import migrations, models
import portal.models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
        migrations.AlterField(
            model_name='book',
            name='image',
            field=models.ImageField(upload_to=portal.models.path_and_rename),
        ),
    ]