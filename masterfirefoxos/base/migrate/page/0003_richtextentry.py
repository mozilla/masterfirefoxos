# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0002_auto_20150116_1205'),
    ]

    operations = [
        migrations.CreateModel(
            name='RichTextEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('text', models.TextField()),
                ('region', models.CharField(max_length=255)),
                ('ordering', models.IntegerField(default=0, verbose_name='ordering')),
                ('parent', models.ForeignKey(related_name='richtextentry_set', to='page.Page')),
            ],
            options={
                'permissions': [],
                'verbose_name': 'rich text entry',
                'abstract': False,
                'ordering': ['ordering'],
                'verbose_name_plural': 'rich text entrys',
                'db_table': 'page_page_richtextentry',
            },
            bases=(models.Model,),
        ),
    ]
