from django.db import models
from django.template.loader import render_to_string
from django.utils import translation
from django.utils.translation import ugettext as _

import jingo
from feincms.module.page.models import Page
from feincms.content.medialibrary.models import MediaFileContent
from jinja2 import Markup


jingo.env.install_gettext_translations(translation)


Page.register_templates(
    {
        'title': 'Content template',
        'path': 'content.html',
        'regions': (
            ('main', 'Main content area'),
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
    title = models.CharField(max_length=255)
    text = models.TextField()
    youtube_id = models.CharField(max_length=100)
    _l10n_fields = ['title', 'text', 'youtube_id']

    class Meta:
        abstract = True

    def render(self, **kwargs):
        return render_to_string(
            'includes/videoparagraph.html',
            {
                'title': _(self.title),
                'text': Markup(_(self.text)),
                'video': _(self.youtube_id)
            }
        )


class MediaParagraphEntry(MediaFileContent):
    title = models.CharField(max_length=255)
    text = models.TextField()
    _l10n_fields = ['title', 'text']

    class Meta:
        abstract = True

    def render(self, **kwargs):
        return render_to_string(
            'includes/mediaparagraph.html',
            {
                'title': _(self.title),
                'text': Markup(_(self.text)),
                'mediafile': self.mediafile
            }
        )


class FAQEntry(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    _l10n_fields = ['question', 'answer']

    class Meta:
        abstract = True

    def render(self, **kwargs):
        return render_to_string(
            'includes/faqentry.html',
            {
                'question': _(self.question),
                'answer': Markup(_(self.answer)),
            }
        )

class RichTextEntry(models.Model):
    text = models.TextField()
    _l10n_fields = ['text']

    class Meta:
        abstract = True

    def render(self, **kwargs):
        return render_to_string(
            'includes/richtext.html',
            {
                'html': Markup(_(self.text)),
            }
        )


Page.create_content_type(RichTextEntry)
Page.create_content_type(MediaParagraphEntry,
                         TYPE_CHOICES=(('default', 'default'),))
Page.create_content_type(FAQEntry)
Page.create_content_type(YouTubeParagraphEntry)
