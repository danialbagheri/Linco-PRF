# Generated by Django 2.2.3 on 2019-11-18 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_auto_20191118_1415'),
    ]

    operations = [
        migrations.AddField(
            model_name='modelchangelogsmodel',
            name='table_id',
            field=models.BigIntegerField(blank=True, db_index=True, default=1),
            preserve_default=False,
        ),
    ]
