import os

from django.db import models
from django.forms import ModelChoiceField, Textarea
from django.utils.safestring import mark_safe

from feincms.admin.item_editor import FeinCMSInline as FeinCMSInlineOld
from feincms.module.medialibrary.fields import MediaFileForeignKey
from feincms.module.medialibrary.models import MediaFile


class CustomMediaFileTypeChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        basename = os.path.basename(obj.file.name)
        basename = basename.rsplit('.')[0]
        return basename


class TinyMCETextArea(Textarea):
    def render(self, name, value, attrs=None):
        widget_code = super(TinyMCETextArea, self).render(
            name, value, attrs)
        return mark_safe(
            '{} <br/><a class="activate-tinymce">Activate TinyMCE</a>'.format(widget_code))

    class Media:
        js = [
            '//tinymce.cachefly.net/4.1/tinymce.min.js',
            'js/init_tinymce.js'
        ]


class FeinCMSInline(FeinCMSInlineOld):
    formfield_overrides = {
        models.TextField: {'widget': TinyMCETextArea},
    }


class MediaFileInline(FeinCMSInline):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if isinstance(db_field, MediaFileForeignKey):
            return CustomMediaFileTypeChoiceField(
                MediaFile.objects.filter(type='image', categories__title='en'),
                required=not db_field.blank, **kwargs)
        return super(MediaFileInline, self).formfield_for_foreignkey(db_field, request, **kwargs)
