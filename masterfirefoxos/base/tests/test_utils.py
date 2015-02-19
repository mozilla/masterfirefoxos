from unittest.mock import Mock, patch

from django.test import override_settings, RequestFactory

from feincms.module.page.models import Page

from .. import models
from .. import utils


def test_entry_strings():
    rich_text_entry = models.RichTextEntry(
        title='title', subheader_2='sub 2', subheader_3='sub 3', text='test text')
    assert utils.entry_strings(rich_text_entry) == ['title', 'sub 2', 'sub 3', 'test text']

    image_paragraph_entry = models.ImageParagraphEntry(
        alt='alt', title='test title', text='test text',
        subheader_2='sub 2', subheader_3='sub 3')
    assert set(utils.entry_strings(image_paragraph_entry)) == set([
        'alt', 'test title', 'test text', 'sub 2', 'sub 3'])

    faq_entry = models.FAQEntry(
        question='test question', answer='test answer')
    assert utils.entry_strings(faq_entry) == [
        'test question', 'test answer']

    youtube_entry = models.YouTubeParagraphEntry(
        title='test title', text='test text', youtube_id='test id',
        subheader_2='sub 2', subheader_3='sub 3')
    assert set(utils.entry_strings(youtube_entry)) == set([
        'test title', 'test text', 'test id', 'sub 2', 'sub 3'])


def test_pages_l10n_template():
    parent = Page(title='Parent Title', slug='parent-slug')
    page = Page(title='Page Title', slug='page-slug')
    page.parent = parent
    parent_entry = models.RichTextEntry(text='<p>Parent Text</p>')
    entry = models.RichTextEntry(text='<p>Page Text</p>')
    parent.content.all_of_type = lambda content_type: [parent_entry]
    page.content.all_of_type = lambda content_type: [entry]
    l10n_template = utils.pages_l10n_template([parent, page])
    assert 'Page path: /parent-slug/\n' in l10n_template
    assert 'Page path: /parent-slug/page-slug/\n' in l10n_template
    assert ('{% blocktrans trimmed %}\nParent Title\n{% endblocktrans %}'
            in l10n_template)
    assert ('{% blocktrans trimmed %}\nPage Title\n{% endblocktrans %}'
            in l10n_template)
    assert ('{% blocktrans trimmed %}\n<p>Parent Text</p>\n{% endblocktrans %}'
            in l10n_template)
    assert ('{% blocktrans trimmed %}\n<p>Page Text</p>\n{% endblocktrans %}'
            in l10n_template)


@patch('masterfirefoxos.base.utils.copy_content_and_children')
@patch('masterfirefoxos.base.utils.Page.objects')
@patch('masterfirefoxos.base.utils.datetime')
def test_copy_tree(mock_datetime, mock_page_objects,
                   mock_copy_content_and_children):
    mock_datetime.now().strftime.return_value = 'date'
    parent = Page()
    page = Page(title='foo bar', slug='sl-ug', active=True, parent=parent)
    assert (utils.copy_tree(page) ==
            mock_copy_content_and_children.return_value)
    mock_page_objects.create.assert_called_with(
        title='Copy of foo bar on date', slug='copy-of-sl-ug-on-date',
        parent=parent, active=False)
    mock_copy_content_and_children.assert_called_with(
        page, mock_page_objects.create.return_value)


@patch('masterfirefoxos.base.utils.copy_content_and_children')
@patch('masterfirefoxos.base.utils.Page.objects')
def test_copy_page_with_parent(mock_page_objects,
                               mock_copy_content_and_children):
    page = Page(title='title', slug='slug', active=False)
    assert (utils.copy_page_with_parent(page, 'parent') ==
            mock_copy_content_and_children.return_value)
    mock_page_objects.create.assert_called_with(
        title='title', slug='slug', parent='parent', active=False)
    mock_copy_content_and_children.assert_called_with(
        page, mock_page_objects.create.return_value)


@patch('masterfirefoxos.base.utils.copy_page_with_parent')
def test_copy_content_and_children(mock_copy_page_with_parent):
    page = Mock()
    page.get_children.return_value = ['child']
    new_page = Mock()
    assert utils.copy_content_and_children(page, new_page) == new_page
    new_page.copy_content_from.assert_called_with(page)
    mock_copy_page_with_parent.assert_called_with('child', new_page)


@patch('masterfirefoxos.base.utils._')
def test_youtube_embed_url_translated_id(mock_gettext):
    mock_gettext.return_value = 'xx-youtube-id'
    request = RequestFactory().get('/xx/introduction/')
    expected = 'https://www.youtube.com/embed/xx-youtube-id'
    assert utils.youtube_embed_url(request, 'en-youtube-id') == expected
    mock_gettext.assert_called_with('en-youtube-id')


@override_settings(LANGUAGE_NAMES={'xx': 'Pirate'})
@patch('masterfirefoxos.base.utils._')
def test_youtube_embed_url_subtitle_querystring(mock_gettext):
    mock_gettext.return_value = 'en-youtube-id'
    request = RequestFactory().get('/xx/introduction/')
    expected = ('https://www.youtube.com/embed/en-youtube-id' +
                '?hl=xx&cc_lang_pref=xx&cc_load_policy=1')
    assert utils.youtube_embed_url(request, 'en-youtube-id') == expected
    mock_gettext.assert_called_with('en-youtube-id')


@patch('masterfirefoxos.base.utils._')
def test_youtube_embed_url_en(mock_gettext):
    mock_gettext.return_value = 'en-youtube-id'
    request = RequestFactory().get('/en/introduction/')
    expected = 'https://www.youtube.com/embed/en-youtube-id'
    assert utils.youtube_embed_url(request, 'en-youtube-id') == expected
    mock_gettext.assert_called_with('en-youtube-id')
