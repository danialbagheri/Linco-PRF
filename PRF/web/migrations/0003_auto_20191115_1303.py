# Generated by Django 2.2.3 on 2019-11-15 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_auto_20191113_1500'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productionjob',
            name='prf_number',
            field=models.IntegerField(null=True, unique=True),
        ),
    ]