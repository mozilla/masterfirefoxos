from django.test import SimpleTestCase

from feincms.module.medialibrary.models import MediaFile
from feincms.module.page.models import Page

from . import models
from . import utils


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


class TestUtils(SimpleTestCase):
    def test_entry_strings(self):
        rich_text_entry = models.RichTextEntry(text='test text')
        self.assertEqual(
            utils.entry_strings(rich_text_entry),
            ['test text'])

        media_paragraph_entry = models.MediaParagraphEntry(
            title='test title', text='test text')
        self.assertEqual(
            utils.entry_strings(media_paragraph_entry),
            ['test title', 'test text'])

        faq_entry = models.FAQEntry(
            question='test question', answer='test answer')
        self.assertEqual(
            utils.entry_strings(faq_entry),
            ['test question', 'test answer'])

        youtube_entry = models.YouTubeParagraphEntry(
            title='test title', text='test text', youtube_id='test id')
        self.assertEqual(
            utils.entry_strings(youtube_entry),
            ['test title', 'test text'])

    def test_pages_l10n_template(self):
        parent = Page(title='Parent Page')
        page = Page(title='Page Title')
        page.parent = parent
        entry = models.RichTextEntry(text='<p>Rich Text</p>')
        page.content.all_of_type = lambda content_type: [entry]
        l10n_template = utils.pages_l10n_template([page])
        self.assertTrue('Parent Page Title: Parent Page' in l10n_template)
        self.assertTrue(
            '{% blocktrans %}Page Title{% endblocktrans %}' in l10n_template)
        self.assertTrue(
            '{% blocktrans trimmed %}\n<p>Rich Text</p>\n{% endblocktrans %}'
            in l10n_template)
        
