# Generated by Django 2.2.3 on 2019-11-20 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0004_auto_20191118_1511'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productionjob',
            name='expected_completion_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
