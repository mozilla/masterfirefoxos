# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0007_auto_20150128_1239'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quizquestion',
            name='image',
        ),
    ]
