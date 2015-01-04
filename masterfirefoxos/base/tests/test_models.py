from feincms.module.medialibrary.models import MediaFile

from .. import models


def test_youtube_paragraph_render():
    test_data = {'title': 'Test Title', 'text': 'test text',
                 'youtube_id': 'test youtube id'}
    rendered = models.YouTubeParagraphEntry(**test_data).render()
    for value in test_data.values():
        assert value in rendered


def test_media_paragraph_render():
    test_data = {'title': 'Test Title', 'text': 'test text'}
    entry = models.MediaParagraphEntry(**test_data)
    entry.mediafile = MediaFile()
    entry.mediafile.get_absolute_url = lambda: 'test mediafile url'
    rendered = entry.render()
    assert'test mediafile url' in rendered
    for value in test_data.values():
        assert value in rendered


def test_faq_render():
    test_data = {'question': 'test question', 'answer': 'test answer'}
    rendered = models.FAQEntry(**test_data).render()
    for value in test_data.values():
        assert value in rendered
