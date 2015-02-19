# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0009_quizquestion_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Locale',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),  # noqa
                ('code', models.CharField(max_length=10, unique=True, choices=[('bn', 'Bengali'), ('hr', 'Croatian'), ('cs', 'Czech'), ('en', 'English'), ('de', 'German'), ('el', 'Greek'), ('hi', 'Hindi'), ('hu', 'Hungarian'), ('it', 'Italian'), ('ja', 'Japanese'), ('pl', 'Polish'), ('pt', 'Portuguese'), ('sr', 'Serbian'), ('es', 'Spanish'), ('ta', 'Tamil'), ('xx', 'Pirate')])),  # noqa
                ('latest_version', models.ForeignKey(blank=True, null=True, to='page.Page')),  # noqa
                ('pending_versions', models.ManyToManyField(blank=True, to='page.Page', related_name='pending_locales', null=True)),  # noqa
                ('versions', models.ManyToManyField(blank=True, to='page.Page', related_name='locales', null=True)),  # noqa
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
