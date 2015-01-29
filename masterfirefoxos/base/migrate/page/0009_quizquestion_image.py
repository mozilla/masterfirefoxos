# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import feincms.module.medialibrary.fields


class Migration(migrations.Migration):

    dependencies = [
        ('medialibrary', '0002_auto_20150128_1239'),
        ('page', '0008_remove_quizquestion_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='quizquestion',
            name='image',
            field=feincms.module.medialibrary.fields.MediaFileForeignKey(blank=True, to='medialibrary.MediaFile', null=True),
            preserve_default=True,
        ),
    ]
