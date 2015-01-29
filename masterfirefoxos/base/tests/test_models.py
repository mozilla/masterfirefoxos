from unittest.mock import patch

from . import MediaFileFactory, ImageFieldFactory
from .. import models


def test_youtube_paragraph_render():
    test_data = {'title': 'Test Title', 'text': 'test text',
                 'youtube_id': 'test youtube id'}
    rendered = models.YouTubeParagraphEntry(**test_data).render()
    for value in test_data.values():
        assert value in rendered


def test_media_paragraph_render():
    test_data = {'title': 'Test Title', 'text': 'test text'}
    entry = models.ImageParagraphEntry(**test_data)
    entry.image = MediaFileFactory()
    with patch('masterfirefoxos.base.helpers.MediaFile') as MediaFileMock:
        with patch('masterfirefoxos.base.helpers.get_thumbnail') as get_thumbnail_mock:
            get_thumbnail_mock.return_value = ImageFieldFactory(url='new_media_url')
            MediaFileMock.objects.filter().exists.return_value = False
            rendered = entry.render()
    assert 'new_media_url' in rendered
    for value in test_data.values():
        assert value in rendered


def test_faq_render():
    test_data = {'question': 'test question', 'answer': 'test answer'}
    rendered = models.FAQEntry(**test_data).render()
    for value in test_data.values():
        assert value in rendered
