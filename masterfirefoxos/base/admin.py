from django.contrib import admin, messages

from feincms.module.medialibrary.admin import MediaFileAdmin as MediaFileAdminOld
from feincms.module.medialibrary.models import MediaFile
from feincms.module.page.admin import PageAdmin as PageAdminOld
from feincms.module.page.models import Page
from feincms.module.page.forms import PageAdminForm as PageAdminFormOld

from .utils import copy_tree


class PageAdminForm(PageAdminFormOld):
    class Media:
        js = [
            '//tinymce.cachefly.net/4.1/tinymce.min.js',
            'js/init_tinymce.js'
        ]


class PageAdmin(PageAdminOld):
    save_on_top = True
    actions = ['copy_tree_admin_action']
    list_display = ['short_title', 'slug', 'is_visible_admin', 'template']
    form = PageAdminForm

    def copy_tree_admin_action(self, request, queryset):
        if len(queryset) != 1:
            self.message_user(request, 'Select only one page to copy', level=messages.ERROR)
            return
        copy_tree(queryset[0])
    copy_tree_admin_action.short_description = 'Copy tree'


admin.site.unregister(Page)
admin.site.register(Page, PageAdmin)


class MediaFileAdmin(MediaFileAdminOld):
    inlines = []
    list_display = ['admin_thumbnail', '__str__', 'formatted_created']

    fieldsets = (
        (None, {'fields': ('file', 'categories')}),
    )


admin.site.unregister(MediaFile)
admin.site.register(MediaFile, MediaFileAdmin)
