# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('medialibrary', '0002_auto_20150128_1239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mediafiletranslation',
            name='language_code',
            field=models.CharField(verbose_name='language', choices=[('bn', 'Bengali'), ('hr', 'Croatian'), ('cs', 'Czech'), ('en', 'English'), ('de', 'German'), ('el', 'Greek'), ('hi', 'Hindi'), ('hu', 'Hungarian'), ('it', 'Italian'), ('ja', 'Japanese'), ('pl', 'Polish'), ('pt', 'Portuguese'), ('sr', 'Serbian'), ('es', 'Spanish'), ('ta', 'Tamil'), ('xx', 'Pirate')], max_length=10, default='bn'),
            preserve_default=True,
        ),
    ]
