# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import feincms.module.medialibrary.fields


class Migration(migrations.Migration):

    dependencies = [
        ('medialibrary', '0002_auto_20150128_1239'),
        ('page', '0006_auto_20150128_0414'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageParagraphEntry',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('alt', models.CharField(blank=True, max_length=255, default='')),
                ('title', models.CharField(max_length=255)),
                ('text', models.TextField()),
                ('region', models.CharField(max_length=255)),
                ('ordering', models.IntegerField(default=0, verbose_name='ordering')),
                ('image', feincms.module.medialibrary.fields.MediaFileForeignKey(to='medialibrary.MediaFile')),
                ('parent', models.ForeignKey(to='page.Page', related_name='imageparagraphentry_set')),
            ],
            options={
                'db_table': 'page_page_imageparagraphentry',
                'abstract': False,
                'ordering': ['ordering'],
                'permissions': [],
                'verbose_name': 'image paragraph entry',
                'verbose_name_plural': 'image paragraph entrys',
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='mediaparagraphentry',
            name='parent',
        ),
        migrations.DeleteModel(
            name='MediaParagraphEntry',
        ),
    ]
