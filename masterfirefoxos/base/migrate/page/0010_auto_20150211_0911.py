# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0009_quizquestion_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='imageparagraphentry',
            name='subheader_2',
            field=models.CharField(max_length=255, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='imageparagraphentry',
            name='subheader_3',
            field=models.CharField(max_length=255, blank=True),
            preserve_default=True,
        ),
    ]
