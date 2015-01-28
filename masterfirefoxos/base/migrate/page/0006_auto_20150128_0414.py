# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0005_auto_20150127_1425'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuizAnswer',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('answer', models.TextField()),
                ('correct', models.BooleanField(default=False)),
                ('region', models.CharField(max_length=255)),
                ('ordering', models.IntegerField(default=0, verbose_name='ordering')),
                ('parent', models.ForeignKey(related_name='quizanswer_set', to='page.Page')),
            ],
            options={
                'ordering': ['ordering'],
                'verbose_name': 'quiz answer',
                'verbose_name_plural': 'quiz answers',
                'permissions': [],
                'db_table': 'page_page_quizanswer',
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='QuizQuestion',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('image', sorl.thumbnail.fields.ImageField(null=True, upload_to='', blank=True)),
                ('question', models.TextField()),
                ('correct_feedback', models.TextField()),
                ('incorrect_feedback', models.TextField()),
                ('partly_correct_feedback', models.TextField()),
                ('region', models.CharField(max_length=255)),
                ('ordering', models.IntegerField(default=0, verbose_name='ordering')),
                ('parent', models.ForeignKey(related_name='quizquestion_set', to='page.Page')),
            ],
            options={
                'ordering': ['ordering'],
                'verbose_name': 'quiz question',
                'verbose_name_plural': 'quiz questions',
                'permissions': [],
                'db_table': 'page_page_quizquestion',
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='mediaparagraphentry',
            name='alt',
            field=models.CharField(max_length=255, default='', blank=True),
            preserve_default=True,
        ),
    ]
