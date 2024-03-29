# Generated by Django 2.1.5 on 2019-01-21 03:40

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('keyphrases', '0002_auto_20190120_2016'),
    ]

    operations = [
        migrations.AddField(
            model_name='keyphrase',
            name='aliases',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=255), blank=True, null=True, size=None),
        ),
        migrations.AlterField(
            model_name='keyphrase',
            name='active',
            field=models.BooleanField(default=False),
        ),
    ]
