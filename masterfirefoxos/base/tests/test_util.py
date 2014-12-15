from unittest.mock import patch

from django.test import SimpleTestCase

from nose.tools import eq_, ok_

from masterfirefoxos.base.tests import PageFactory
from masterfirefoxos.base.utils import copy_tree


class TestCopyTree(SimpleTestCase):
    @patch('masterfirefoxos.base.utils.Page.copy_content_from')
    @patch('masterfirefoxos.base.utils.datetime')
    def test_no_parent(self, mock_datetime, mock_copy_content_from):
        mock_datetime.now().strftime.return_value = 'date'
        page = PageFactory(title='foo bar', slug='sl-ug', active=True)
        new_page = copy_tree(page)
        ok_(page.id != new_page.id)
        eq_(new_page.title, 'Copy of foo bar on date')
        eq_(new_page.slug, 'copy-of-sl-ug-on-date')
        eq_(new_page.active, False)
        mock_copy_content_from.assert_called_with(page)

    def test_with_parent(self):
        parent_page = PageFactory()
        page = PageFactory(parent=parent_page)
        new_parent_page = PageFactory()
        new_page = copy_tree(page, new_parent_page)
        ok_(page.id != new_page.id)
        eq_(new_page.title, page.title)
        eq_(new_page.slug, page.slug)

    def test_copy_tree(self):
        page = PageFactory()
        child_1 = PageFactory(parent=page)
        child_2 = PageFactory(parent=page)
        grandchild = PageFactory(parent=child_1)
        new_page = copy_tree(page)
        new_child_1, new_grandchild, new_child_2 = new_page.get_descendants()
        ok_(child_1.id != new_child_1.id)
        eq_(child_1.title, new_child_1.title)
        eq_(child_1.slug, new_child_1.slug)
        eq_(new_child_1.parent, new_page)
        ok_(child_2.id != new_child_2.id)
        eq_(child_2.title, new_child_2.title)
        eq_(child_2.slug, new_child_2.slug)
        eq_(new_child_2.parent, new_page)
        ok_(grandchild.id != new_grandchild.id)
        eq_(grandchild.title, new_grandchild.title)
        eq_(grandchild.slug, new_grandchild.slug)
        eq_(new_grandchild.parent, new_child_1)
