from unittest.mock import patch

from feincms.module.page.models import Page

from masterfirefoxos.base.admin import PageAdmin


@patch('masterfirefoxos.base.admin.copy_tree')
@patch('masterfirefoxos.base.admin.PageAdmin.message_user')
def test_copy_tree_action_empty_queryset(mock_message_user, mock_copy_tree):
    page_admin = PageAdmin(Page, None)
    queryset = Page.objects.none()
    page_admin.copy_tree_admin_action('request', queryset)
    mock_message_user.assert_called()
    assert not mock_copy_tree.called


@patch('masterfirefoxos.base.admin.copy_tree')
@patch('masterfirefoxos.base.admin.PageAdmin.message_user')
def test_copy_tree_action(mock_message_user, mock_copy_tree):
    page_admin = PageAdmin(Page, None)
    page_admin.copy_tree_admin_action('request', ['page'])
    assert not mock_message_user.called
    mock_copy_tree.assert_called_with('page')
