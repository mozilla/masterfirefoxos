from unittest.mock import Mock, patch

from feincms.module.page.models import Page

from .. import models
from .. import utils


def test_entry_strings():
    rich_text_entry = models.RichTextEntry(text='test text')
    assert utils.entry_strings(rich_text_entry) == ['test text']

    media_paragraph_entry = models.ImageParagraphEntry(
        alt='alt', title='test title', text='test text')
    assert utils.entry_strings(media_paragraph_entry) == [
        'alt', 'test title', 'test text']

    faq_entry = models.FAQEntry(
        question='test question', answer='test answer')
    assert utils.entry_strings(faq_entry) == [
        'test question', 'test answer']

    youtube_entry = models.YouTubeParagraphEntry(
        title='test title', text='test text', youtube_id='test id')
    assert utils.entry_strings(youtube_entry) == [
        'test title', 'test text', 'test id']


def test_pages_l10n_template():
    parent = Page(title='Parent Page')
    page = Page(title='Page Title')
    page.parent = parent
    entry = models.RichTextEntry(text='<p>Rich Text</p>')
    page.content.all_of_type = lambda content_type: [entry]
    l10n_template = utils.pages_l10n_template([page])
    assert 'Parent Page Title: Parent Page' in l10n_template
    assert ('{% blocktrans trimmed %}\nPage Title\n{% endblocktrans %}'
            in l10n_template)
    assert ('{% blocktrans trimmed %}\n<p>Rich Text</p>\n{% endblocktrans %}'
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
