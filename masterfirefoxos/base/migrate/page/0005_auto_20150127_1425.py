# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0004_auto_20150116_1254'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mediaparagraphentry',
            name='mediafile',
        ),
        migrations.RemoveField(
            model_name='mediaparagraphentry',
            name='type',
        ),
        migrations.AddField(
            model_name='mediaparagraphentry',
            name='image',
            field=sorl.thumbnail.fields.ImageField(upload_to='', null=True),
            preserve_default=True,
        ),
    ]
