from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.utils import translation
from django.utils.translation import ugettext as _

from jinja2 import Markup
from feincms.module.medialibrary.fields import MediaFileForeignKey
from feincms.module.medialibrary.models import MediaFile
from feincms.module.page.models import Page

from .forms import FeinCMSInline, MediaFileInline
from .utils import youtube_embed_url



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
    subheader_2 = models.CharField(max_length=255, blank=True)
    subheader_3 = models.CharField(max_length=255, blank=True)
    text = models.TextField(help_text='HTML is allowed.')
    youtube_id = models.CharField(max_length=100)
    _l10n_fields = ['title', 'text', 'subheader_2', 'subheader_3']

    class Meta:
        abstract = True

    def render(self, **kwargs):
        return render_to_string(
            'includes/videoparagraph.html',
            {
                'title': _(self.title),
                'subheader_2': _(self.subheader_2) if self.subheader_2 else '',
                'subheader_3': _(self.subheader_3) if self.subheader_3 else '',
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
    subheader_2 = models.CharField(max_length=255, blank=True)
    subheader_3 = models.CharField(max_length=255, blank=True)
    text = models.TextField(help_text='HTML is allowed.')
    _l10n_fields = ['alt', 'title', 'text', 'subheader_2', 'subheader_3']

    class Meta:
        abstract = True

    def render(self, **kwargs):
        return render_to_string(
            'includes/imageparagraph.html',
            {
                'alt': _(self.alt) if self.alt else '',
                'title': _(self.title),
                'text': Markup(_(self.text)),
                'subheader_2': _(self.subheader_2) if self.subheader_2 else '',
                'subheader_3': _(self.subheader_3) if self.subheader_3 else '',
                'image': self.image,
            }
        )


class FAQEntry(models.Model):
    feincms_item_editor_inline = FeinCMSInline
    question = models.CharField(max_length=255)
    answer = models.TextField(help_text='HTML is allowed.')
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
    title = models.CharField(max_length=255, blank=True)
    subheader_2 = models.CharField(max_length=255, blank=True)
    subheader_3 = models.CharField(max_length=255, blank=True)
    text = models.TextField(help_text='HTML is allowed.')
    _l10n_fields = ['text', 'title', 'subheader_2', 'subheader_3']

    class Meta:
        abstract = True

    def render(self, **kwargs):
        return render_to_string(
            'includes/richtextentry.html',
            {
                'title': _(self.title) if self.title else '',
                'subheader_2': _(self.subheader_2) if self.subheader_2 else '',
                'subheader_3': _(self.subheader_3) if self.subheader_3 else '',
                'text': Markup(_(self.text)),
            }
        )


class QuizQuestion(models.Model):
    feincms_item_editor_inline = MediaFileInline
    image = MediaFileForeignKey(
        MediaFile,
        limit_choices_to=models.Q(type='image', categories__title='en'),
        blank=True, null=True)
    question = models.TextField(help_text='HTML is allowed.')
    correct_feedback = models.TextField(help_text='HTML is allowed.')
    incorrect_feedback = models.TextField(help_text='HTML is allowed.')
    partly_correct_feedback = models.TextField(help_text='HTML is allowed.')
    _l10n_fields = ['question', 'correct_feedback', 'incorrect_feedback',
                    'partly_correct_feedback']

    class Meta:
        abstract = True

    def render(self, **kwargs):
        return render_to_string(
            'includes/quizquestion.html', {'question': self})


class QuizAnswer(models.Model):
    feincms_item_editor_inline = FeinCMSInline
    answer = models.TextField(help_text='HTML is allowed.')
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


@receiver(pre_save, dispatch_uid='trim_content_signal')
def trim_content(sender, instance, **kwargs):
    """Trim spaces from TextFields and CharFields before saving."""
    if sender in Page._feincms_content_types:
        for field in instance._meta.fields:
            if (isinstance(field, models.TextField) or
                isinstance(field, models.CharField)):
                value = getattr(instance, field.name, '')
                setattr(instance, field.name, value.strip())


class Locale(models.Model):
    code = models.CharField(max_length=10, choices=settings.LANGUAGES, unique=True)
    latest_version = models.ForeignKey(
        Page, blank=True, null=True,
        limit_choices_to={'parent__isnull': True})
    versions = models.ManyToManyField(
        Page, blank=True, null=True,
        limit_choices_to={'parent__isnull': True},
        related_name='locales')
    pending_versions = models.ManyToManyField(
        Page, blank=True, null=True,
        limit_choices_to={'parent__isnull': True},
        related_name='pending_locales')

    def __str__(self):
        return '{} ({})'.format(settings.LANGUAGE_NAMES[self.code], self.code)

    class Meta:
        ordering = ('code',)
