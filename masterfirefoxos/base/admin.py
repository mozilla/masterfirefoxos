from django.contrib import admin, messages

from feincms.module.page.models import Page
from feincms.module.page.admin import PageAdmin as PageAdminOld

from .utils import copy_tree


admin.site.unregister(Page)


class PageAdmin(PageAdminOld):
    save_on_top = True
    actions = ['copy_tree_admin_action']
    list_display = ['short_title', 'slug', 'is_visible_admin', 'template']


    def copy_tree_admin_action(self, request, queryset):
        if len(queryset) != 1:
            self.message_user(request, 'Select only one page to copy', level=messages.ERROR)
            return
        copy_tree(queryset[0])
    copy_tree_admin_action.short_description = 'Copy tree'

admin.site.register(Page, PageAdmin)
