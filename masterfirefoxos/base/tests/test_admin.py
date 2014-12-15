from unittest.mock import patch

from django.test import SimpleTestCase

from feincms.module.page.models import Page
from nose.tools import ok_

from masterfirefoxos.base.admin import PageAdmin
from masterfirefoxos.base.tests import PageFactory


class TestAdminActions(SimpleTestCase):

    @patch('masterfirefoxos.base.admin.copy_tree')
    @patch('masterfirefoxos.base.admin.PageAdmin.message_user')
    def test_copy_tree_action_empty_queryset(self, mock_message_user, mock_copy_tree):
        page_admin = PageAdmin(Page, None)
        queryset = Page.objects.none()
        page_admin.copy_tree_admin_action('request', queryset)
        mock_message_user.assert_called()
        ok_(not mock_copy_tree.called)

    @patch('masterfirefoxos.base.admin.copy_tree')
    @patch('masterfirefoxos.base.admin.PageAdmin.message_user')
    def test_copy_tree_action(self, mock_message_user, mock_copy_tree):
        page_admin = PageAdmin(Page, None)
        page = PageFactory.create()
        queryset = Page.objects.filter(id=page.id)
        page_admin.copy_tree_admin_action('request', queryset)
        ok_(not mock_message_user.called)
        mock_copy_tree.assert_called_with(page)
