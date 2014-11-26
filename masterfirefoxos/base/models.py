from django.db import models
from django.template.loader import render_to_string
from django.utils.translation import ugettext as _

from feincms.module.page.models import Page
from feincms.content.richtext.models import RichTextContent
from feincms.content.medialibrary.models import MediaFileContent

import fields


Page.register_templates(
    {
        'title': 'Content template',
        'path': 'content.html',
        'regions': (
            ('main', 'Main content area'),
            ('sidebar', 'Sidebar', 'inherited'),
        ),
    },
    {
        'title': 'Home template',
        'path': 'home.html',
        'regions': (
            ('main', 'Main content area'),
        ),
    }
)


class YouTubeParagraphEntry(models.Model):
    title = fields.LocalizableCharField(max_length=255)
    text = fields.LocalizableTextField()
    youtube_id = fields.LocalizableCharField(max_length=100)

    class Meta:
        abstract = True

    def render(self, **kwargs):
        return render_to_string(
            'videoparagraph.html',
            {
                'title': _(self.title),
                'text': _(self.text),
                'video': self.youtube_id
            }
        )


class MediaParagraphEntry(MediaFileContent):
    title = fields.LocalizableCharField(max_length=255)
    text = fields.LocalizableTextField()

    class Meta:
        abstract = True

    def render(self, **kwargs):
        return render_to_string(
            'mediaparagraph.html',
            {
                'title': _(self.title),
                'text': _(self.text),
                'mediafile': self.mediafile
            }
        )


class FAQEntry(models.Model):
    question = fields.LocalizableCharField(max_length=255)
    answer = fields.LocalizableTextField(max_length=255)

    class Meta:
        abstract = True

    def render(self, **kwargs):
        return render_to_string(
            'faqentry.html',
            {
                'question': _(self.question),
                'answer': _(self.answer),
            }
        )

Page.create_content_type(RichTextContent)
Page.create_content_type(MediaParagraphEntry,
                         TYPE_CHOICES=(('default', 'default'),))
Page.create_content_type(FAQEntry)
Page.create_content_type(YouTubeParagraphEntry)
