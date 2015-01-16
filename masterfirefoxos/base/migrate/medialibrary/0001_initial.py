# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import feincms.translations
import feincms.extensions


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('title', models.CharField(max_length=200, verbose_name='title')),
                ('slug', models.SlugField(max_length=150, verbose_name='slug')),
                ('parent', models.ForeignKey(related_name='children', to='medialibrary.Category', verbose_name='parent', null=True, blank=True)),
            ],
            options={
                'ordering': ['parent__title', 'title'],
                'verbose_name_plural': 'categories',
                'verbose_name': 'category',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MediaFile',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('file', models.FileField(max_length=255, verbose_name='file', upload_to='medialibrary/%Y/%m/')),
                ('type', models.CharField(max_length=12, editable=False, choices=[('image', 'Image'), ('video', 'Video'), ('audio', 'Audio'), ('pdf', 'PDF document'), ('swf', 'Flash'), ('txt', 'Text'), ('rtf', 'Rich Text'), ('zip', 'Zip archive'), ('doc', 'Microsoft Word'), ('xls', 'Microsoft Excel'), ('ppt', 'Microsoft PowerPoint'), ('other', 'Binary')], verbose_name='file type')),
                ('created', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('copyright', models.CharField(max_length=200, blank=True, verbose_name='copyright')),
                ('file_size', models.IntegerField(editable=False, null=True, blank=True, verbose_name='file size')),
                ('categories', models.ManyToManyField(to='medialibrary.Category', null=True, blank=True, verbose_name='categories')),
            ],
            options={
                'abstract': False,
                'ordering': ['-created'],
                'verbose_name_plural': 'media files',
                'verbose_name': 'media file',
            },
            bases=(models.Model, feincms.extensions.ExtensionsMixin, feincms.translations.TranslatedObjectMixin),
        ),
        migrations.CreateModel(
            name='MediaFileTranslation',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('language_code', models.CharField(default='bn', max_length=10, choices=[('bn', 'Bengali'), ('hr', 'Croatian'), ('cz', 'Czech'), ('en', 'English'), ('de', 'German'), ('el', 'Greek'), ('hi', 'Hindi'), ('hu', 'Hungarian'), ('it', 'Italian'), ('pl', 'Polish'), ('pt', 'Portuguese'), ('sr', 'Serbian'), ('es', 'Spanish'), ('ta', 'Tamil')], verbose_name='language')),
                ('caption', models.CharField(max_length=200, verbose_name='caption')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('parent', models.ForeignKey(related_name='translations', to='medialibrary.MediaFile')),
            ],
            options={
                'verbose_name': 'media file translation',
                'verbose_name_plural': 'media file translations',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='mediafiletranslation',
            unique_together=set([('parent', 'language_code')]),
        ),
    ]
