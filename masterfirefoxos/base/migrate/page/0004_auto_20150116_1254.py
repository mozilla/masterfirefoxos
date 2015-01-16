# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0003_richtextentry'),
    ]

    operations = [
        migrations.AlterField(
            model_name='faqentry',
            name='answer',
            field=models.TextField(),
            preserve_default=True,
        ),
    ]
