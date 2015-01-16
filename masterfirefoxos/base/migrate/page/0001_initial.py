# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import feincms.extensions
import feincms.module.medialibrary.fields
import feincms.contrib.richtext
import feincms.module.mixins


class Migration(migrations.Migration):

    dependencies = [
        ('medialibrary', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FAQEntry',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('question', models.CharField(max_length=255)),
                ('answer', models.CharField(max_length=255)),
                ('region', models.CharField(max_length=255)),
                ('ordering', models.IntegerField(default=0, verbose_name='ordering')),
            ],
            options={
                'verbose_name': 'faq entry',
                'abstract': False,
                'ordering': ['ordering'],
                'verbose_name_plural': 'faq entrys',
                'db_table': 'page_page_faqentry',
                'permissions': [],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MediaParagraphEntry',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('title', models.CharField(max_length=255)),
                ('text', models.TextField()),
                ('region', models.CharField(max_length=255)),
                ('ordering', models.IntegerField(default=0, verbose_name='ordering')),
                ('type', models.CharField(default='default', verbose_name='type', choices=[('default', 'default')], max_length=20)),
                ('mediafile', feincms.module.medialibrary.fields.MediaFileForeignKey(verbose_name='media file', to='medialibrary.MediaFile', related_name='+')),
            ],
            options={
                'verbose_name': 'media paragraph entry',
                'abstract': False,
                'ordering': ['ordering'],
                'verbose_name_plural': 'media paragraph entrys',
                'db_table': 'page_page_mediaparagraphentry',
                'permissions': [],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('active', models.BooleanField(default=True, verbose_name='active')),
                ('title', models.CharField(help_text='This title is also used for navigation menu items.', verbose_name='title', max_length=200)),
                ('slug', models.SlugField(help_text='This is used to build the URL for this page', verbose_name='slug', max_length=150)),
                ('in_navigation', models.BooleanField(default=False, verbose_name='in navigation')),
                ('override_url', models.CharField(blank=True, help_text="Override the target URL. Be sure to include slashes at the beginning and at the end if it is a local URL. This affects both the navigation and subpages' URLs.", verbose_name='override URL', max_length=255)),
                ('redirect_to', models.CharField(blank=True, help_text='Target URL for automatic redirects or the primary key of a page.', verbose_name='redirect to', max_length=255)),
                ('_cached_url', models.CharField(blank=True, default='', verbose_name='Cached URL', db_index=True, editable=False, max_length=255)),
                ('template_key', models.CharField(default='content.html', verbose_name='template', choices=[('content.html', 'Content template'), ('home.html', 'Home template')], max_length=255)),
                ('parent', models.ForeignKey(blank=True, verbose_name='Parent', to='page.Page', null=True, related_name='children')),
            ],
            options={
                'verbose_name': 'page',
                'verbose_name_plural': 'pages',
                'ordering': ['tree_id', 'lft'],
            },
            bases=(models.Model, feincms.extensions.ExtensionsMixin, feincms.module.mixins.ContentModelMixin),
        ),
        migrations.CreateModel(
            name='RichTextEntry',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('text', feincms.contrib.richtext.RichTextField(blank=True, verbose_name='text')),
                ('region', models.CharField(max_length=255)),
                ('ordering', models.IntegerField(default=0, verbose_name='ordering')),
                ('parent', models.ForeignKey(to='page.Page', related_name='richtextentry_set')),
            ],
            options={
                'verbose_name': 'rich text entry',
                'abstract': False,
                'ordering': ['ordering'],
                'verbose_name_plural': 'rich text entrys',
                'db_table': 'page_page_richtextentry',
                'permissions': [],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='YouTubeParagraphEntry',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('title', models.CharField(max_length=255)),
                ('text', models.TextField()),
                ('youtube_id', models.CharField(max_length=100)),
                ('region', models.CharField(max_length=255)),
                ('ordering', models.IntegerField(default=0, verbose_name='ordering')),
                ('parent', models.ForeignKey(to='page.Page', related_name='youtubeparagraphentry_set')),
            ],
            options={
                'verbose_name': 'you tube paragraph entry',
                'abstract': False,
                'ordering': ['ordering'],
                'verbose_name_plural': 'you tube paragraph entrys',
                'db_table': 'page_page_youtubeparagraphentry',
                'permissions': [],
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='mediaparagraphentry',
            name='parent',
            field=models.ForeignKey(to='page.Page', related_name='mediaparagraphentry_set'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='faqentry',
            name='parent',
            field=models.ForeignKey(to='page.Page', related_name='faqentry_set'),
            preserve_default=True,
        ),
    ]
