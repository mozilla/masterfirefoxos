# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0012_auto_20150211_1114'),
    ]

    operations = [
        migrations.AlterField(
            model_name='faqentry',
            name='answer',
            field=models.TextField(help_text='HTML is allowed.'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='imageparagraphentry',
            name='text',
            field=models.TextField(help_text='HTML is allowed.'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='quizanswer',
            name='answer',
            field=models.TextField(help_text='HTML is allowed.'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='quizquestion',
            name='correct_feedback',
            field=models.TextField(help_text='HTML is allowed.'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='quizquestion',
            name='incorrect_feedback',
            field=models.TextField(help_text='HTML is allowed.'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='quizquestion',
            name='partly_correct_feedback',
            field=models.TextField(help_text='HTML is allowed.'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='quizquestion',
            name='question',
            field=models.TextField(help_text='HTML is allowed.'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='richtextentry',
            name='text',
            field=models.TextField(help_text='HTML is allowed.'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='youtubeparagraphentry',
            name='text',
            field=models.TextField(help_text='HTML is allowed.'),
            preserve_default=True,
        ),
    ]
