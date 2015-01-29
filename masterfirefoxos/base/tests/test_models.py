from sorl.thumbnail import ImageField

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
    entry.image = ImageField()
    entry.image.url = 'test mediafile url'
    rendered = entry.render()
    assert 'test mediafile url' in rendered
    for value in test_data.values():
        assert value in rendered


def test_faq_render():
    test_data = {'question': 'test question', 'answer': 'test answer'}
    rendered = models.FAQEntry(**test_data).render()
    for value in test_data.values():
        assert value in rendered
