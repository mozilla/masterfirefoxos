# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0011_auto_20150211_0919'),
    ]

    operations = [
        migrations.AddField(
            model_name='richtextentry',
            name='subheader_2',
            field=models.CharField(max_length=255, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='richtextentry',
            name='subheader_3',
            field=models.CharField(max_length=255, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='richtextentry',
            name='title',
            field=models.CharField(max_length=255, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='richtextentry',
            name='text',
            field=models.TextField(help_text='Yo'),
            preserve_default=True,
        ),
    ]
