from datetime import datetime

from django.contrib.staticfiles.templatetags.staticfiles import static as static_helper
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

