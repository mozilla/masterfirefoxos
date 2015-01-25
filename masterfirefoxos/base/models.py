from django.db import models
from django.template.loader import render_to_string
from django.utils import translation
from django.utils.translation import ugettext as _

import jingo
from feincms.module.page.models import Page
from jinja2 import Markup
from sorl.thumbnail import ImageField

from .inlines import QuizQuestionInline

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


<<<<<<< HEAD
class MediaParagraphEntry(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    image = ImageField(null=True)
    _l10n_fields = ['title', 'text']
=======
class MediaParagraphEntry(MediaFileContent):
    #alt = models.CharField(max_length=255)  # TODO: migration
    title = models.CharField(max_length=255)
    text = models.TextField()
    _l10n_fields = ['alt', 'title', 'text']
>>>>>>> Add Quiz models, templates, admin, and legacy

    class Meta:
        abstract = True

    def render(self, **kwargs):
        return render_to_string(
            'includes/mediaparagraph.html',
            {
                #'alt': _(self.alt),
                'title': _(self.title),
                'text': Markup(_(self.text)),
                'image': self.image,
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

<<<<<<< HEAD
class RichTextEntry(models.Model):
    text = models.TextField()
=======

class QuizQuestion(models.Model):
    question = models.TextField()
    correct_feedback = models.TextField()
    incorrect_feedback = models.TextField()
    partly_correct_feedback = models.TextField(blank=True)
    _l10n_fields = ['question', 'correct_feedback', 'incorrect_feedback',
                    'partly_correct_feedback']

    def __str__(self):
        return self.question


class QuizAnswer(models.Model):
    question = models.ForeignKey(QuizQuestion, related_name='answers')
    answer = models.TextField()
    correct = models.BooleanField(default=False)
    _l10n_fields = ['answer']


class QuizQuestionEntry(models.Model):
    question = models.ForeignKey(QuizQuestion)
    feincms_item_editor_inline = QuizQuestionInline

    class Meta:
        abstract = True

    def render(self, **kwargs):
        return render_to_string(
            'quizquestion.html', {'question': self.question})


class MediaQuizQuestionEntry(MediaFileContent):
    alt = models.CharField(blank=True, max_length=255)
    question = models.ForeignKey(QuizQuestion)
    feincms_item_editor_inline = QuizQuestionInline
    _l10n_fields = ['alt']

    class Meta:
        abstract = True

    def render(self, **kwargs):
        return render_to_string(
            'mediaquizquestion.html',
            {
                'alt': _(self.alt),
                'mediafile': self.mediafile,
                'question': self.question
            }
        ) 


class RichTextEntry(RichTextContent):
>>>>>>> Add Quiz models, templates, admin, and legacy
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
Page.create_content_type(MediaParagraphEntry)
Page.create_content_type(FAQEntry)
Page.create_content_type(YouTubeParagraphEntry)
Page.create_content_type(QuizQuestionEntry)
Page.create_content_type(MediaQuizQuestionEntry,
                         TYPE_CHOICES=(('default', 'default'),))
