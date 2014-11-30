from django.db import models
from django.template.loader import render_to_string


from feincms.module.page.models import Page
from feincms.content.richtext.models import RichTextContent
from feincms.content.medialibrary.models import MediaFileContent

Page.register_extensions(
)

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
    title = models.CharField(max_length=255)
    text = models.TextField()
    youtube_id = models.CharField(max_length=100)

    class Meta:
        abstract = True

    def render(self, **kwargs):
        return render_to_string(
            'videoparagraph.html',
            {
                'title': self.title,
                'text': self.text,
                'video': self.youtube_id
            }
        )


class MediaParagraphEntry(MediaFileContent):
    title = models.CharField(max_length=255)
    text = models.TextField()

    class Meta:
        abstract = True

    def render(self, **kwargs):
        return render_to_string(
            'mediaparagraph.html',
            {
                'title': self.title,
                'text': self.text,
                'mediafile': self.mediafile
            }
        )


class FAQEntry(models.Model):
    question = models.CharField(max_length=255)
    answer = models.CharField(max_length=255)

    class Meta:
        abstract = True

    def render(self, **kwargs):
        return render_to_string(
            'faqentry.html',
            {
                'question': self.question,
                'answer': self.answer,
            }
        )


Page.create_content_type(RichTextContent)
Page.create_content_type(MediaParagraphEntry,
                         TYPE_CHOICES=(('default', 'default'),))
Page.create_content_type(FAQEntry)
Page.create_content_type(YouTubeParagraphEntry)
