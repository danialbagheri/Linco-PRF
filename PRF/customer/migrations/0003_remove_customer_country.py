# Generated by Django 2.2.3 on 2019-11-20 09:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0002_customer_country'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='country',
        ),
    ]
