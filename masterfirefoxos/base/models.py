from django.db import models
from django.template.loader import render_to_string
from django.utils import translation
from django.utils.translation import ugettext as _

import jingo
from jinja2 import Markup
from feincms.module.medialibrary.fields import MediaFileForeignKey
from feincms.module.medialibrary.models import MediaFile
from feincms.module.page.models import Page

from .forms import FeinCMSInline, MediaFileInline
from .utils import youtube_embed_url


jingo.env.install_gettext_translations(translation)

Page.register_templates(
    {
        'title': 'Content template',
        'path': 'content.html',
        'regions': (
            ('main', 'Main content area'),
            ('homepage', 'Homepage navigation'),
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
    feincms_item_editor_inline = FeinCMSInline
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
                'video': youtube_embed_url(
                    kwargs.get('request'), self.youtube_id)
            }
        )


class ImageParagraphEntry(models.Model):
    feincms_item_editor_inline = MediaFileInline
    image = MediaFileForeignKey(MediaFile)
    alt = models.CharField(max_length=255, blank=True, default='')
    title = models.CharField(max_length=255)
    text = models.TextField()
    _l10n_fields = ['alt', 'title', 'text']

    class Meta:
        abstract = True

    def render(self, **kwargs):
        return render_to_string(
            'includes/imageparagraph.html',
            {
                'alt': _(self.alt) if self.alt else '',
                'title': _(self.title),
                'text': Markup(_(self.text)),
                'image': self.image,
            }
        )


class FAQEntry(models.Model):
    feincms_item_editor_inline = FeinCMSInline
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
    feincms_item_editor_inline = FeinCMSInline
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


class QuizQuestion(models.Model):
    feincms_item_editor_inline = MediaFileInline
    image = MediaFileForeignKey(
        MediaFile,
        limit_choices_to=models.Q(type='image', categories__title='en'),
        blank=True, null=True)
    question = models.TextField()
    correct_feedback = models.TextField()
    incorrect_feedback = models.TextField()
    partly_correct_feedback = models.TextField()
    _l10n_fields = ['question', 'correct_feedback', 'incorrect_feedback',
                    'partly_correct_feedback']

    class Meta:
        abstract = True

    def render(self, **kwargs):
        return render_to_string(
            'includes/quizquestion.html', {'question': self})


class QuizAnswer(models.Model):
    feincms_item_editor_inline = FeinCMSInline
    answer = models.TextField()
    correct = models.BooleanField(default=False)
    _l10n_fields = ['answer']

    class Meta:
        abstract = True

    def render(self, **kwargs):
        return render_to_string(
            'includes/quizanswer.html', {'answer': self})


Page.create_content_type(RichTextEntry)
Page.create_content_type(ImageParagraphEntry)
Page.create_content_type(FAQEntry)
Page.create_content_type(YouTubeParagraphEntry)
Page.create_content_type(QuizQuestion)
Page.create_content_type(QuizAnswer)
