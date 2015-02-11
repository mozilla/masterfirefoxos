# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0010_auto_20150211_0911'),
    ]

    operations = [
        migrations.AddField(
            model_name='youtubeparagraphentry',
            name='subheader_2',
            field=models.CharField(blank=True, max_length=255),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='youtubeparagraphentry',
            name='subheader_3',
            field=models.CharField(blank=True, max_length=255),
            preserve_default=True,
        ),
    ]
