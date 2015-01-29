# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import masterfirefoxos.settings.base


class Migration(migrations.Migration):

    dependencies = [
        ('medialibrary', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mediafile',
            name='file',
            field=models.FileField(upload_to=masterfirefoxos.settings.base.media_files_unique_path, max_length=255, verbose_name='file'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='mediafiletranslation',
            name='language_code',
            field=models.CharField(default='bn', max_length=10, verbose_name='language', choices=[('bn', 'Bengali'), ('hr', 'Croatian'), ('cs', 'Czech'), ('en', 'English'), ('de', 'German'), ('el', 'Greek'), ('hi', 'Hindi'), ('hu', 'Hungarian'), ('it', 'Italian'), ('pl', 'Polish'), ('pt', 'Portuguese'), ('sr', 'Serbian'), ('es', 'Spanish'), ('ta', 'Tamil'), ('xx', 'Pirate')]),
            preserve_default=True,
        ),
    ]
