from datetime import datetime

from django.conf import settings
from django.contrib.staticfiles.templatetags.staticfiles import static as static_helper
from django.utils.translation import activate as dj_activate

from feincms.templatetags.feincms_tags import feincms_render_region
from jingo import register
from jinja2 import Markup


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
    for version, data in settings.VERSIONS_LOCALE_MAP.items():
        if data['slug'] == request.path.split('/')[2]:
            return version
