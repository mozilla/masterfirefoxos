from django.test import SimpleTestCase

from feincms.module.medialibrary.models import MediaFile

from . import models


class TestYouTubeParagraphEntry(SimpleTestCase):
    def test_render(self):
        test_data = {'title': 'Test Title', 'text': 'test text',
                     'youtube_id': 'test youtube id'}
        rendered = models.YouTubeParagraphEntry(**test_data).render()
        for value in test_data.values():
            self.assertTrue(value in rendered)


class TestMediaParagraphEntry(SimpleTestCase):
    def test_render(self):
        test_data = {'title': 'Test Title', 'text': 'test text'}
        entry = models.MediaParagraphEntry(**test_data)
        entry.mediafile = MediaFile()
        entry.mediafile.get_absolute_url = lambda: 'test mediafile url'
        rendered = entry.render()
        self.assertTrue('test mediafile url' in rendered)
        for value in test_data.values():
            self.assertTrue(value in rendered)


class TestFAQEntry(SimpleTestCase):
    def test_render(self):
        test_data = {'question': 'test question', 'answer': 'test answer'}
        rendered = models.FAQEntry(**test_data).render()
        for value in test_data.values():
            self.assertTrue(value in rendered)
