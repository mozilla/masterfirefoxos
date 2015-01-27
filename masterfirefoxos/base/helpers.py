import os
from datetime import datetime

from django.conf import settings
from django.contrib.staticfiles.templatetags.staticfiles import static as static_helper
from django.utils.translation import activate as dj_activate, get_language

from feincms.module.medialibrary.models import MediaFile
from feincms.templatetags.feincms_tags import feincms_render_region
from jingo import register
from jinja2 import Markup
from sorl.thumbnail import get_thumbnail


static = register.function(static_helper)


@register.function
def render_region(feincms_page, region, request):
    return Markup(feincms_render_region(None, feincms_page, region, request))


@register.function
def current_year():
    return datetime.now().strftime('%Y')


@register.function
def activate(language):
    dj_activate(language)
    return ''


@register.function
def active_version(request):
    slug = request.path.split('/')[2]
    for version, data in settings.VERSIONS_LOCALE_MAP.items():
        if data['slug'] == slug:
            return version


@register.function
def get_image_url(img, geometry=None, locale=None):
    if not locale:
        locale = get_language()
    url = img.file.url

    basename = os.path.basename(img.file.name).split('__')[0]

    query = MediaFile.objects.filter(
        file__startswith='medialibrary/' + basename + '__',
        categories__title=locale)

    if query.exists():
        img = query.first()
        url = img.file.url

    if geometry:
        img = get_thumbnail(img.file, geometry, quality=90)
        url = img.url

    return url
