# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-12 09:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logos', '0003_auto_20171111_2123'),
    ]

    operations = [
        migrations.AddField(
            model_name='logoanalyze',
            name='pop_logo_name_1',
            field=models.CharField(default='Unknown', max_length=200),
        ),
        migrations.AddField(
            model_name='logoanalyze',
            name='pop_logo_name_2',
            field=models.CharField(default='Unknown', max_length=200),
        ),
        migrations.AddField(
            model_name='logoanalyze',
            name='pop_logo_name_3',
            field=models.CharField(default='Unknown', max_length=200),
        ),
        migrations.AddField(
            model_name='logoanalyze',
            name='pop_precision_1',
            field=models.CharField(default='0.0', max_length=20),
        ),
        migrations.AddField(
            model_name='logoanalyze',
            name='pop_precision_2',
            field=models.CharField(default='0.0', max_length=20),
        ),
        migrations.AddField(
            model_name='logoanalyze',
            name='pop_precision_3',
            field=models.CharField(default='0.0', max_length=20),
        ),
    ]
