from feincms.templatetags.feincms_tags import feincms_render_region
from jingo import register
from jinja2 import Markup


@register.function
def render_region(feincms_page, region, request):
    return Markup(feincms_render_region(None, feincms_page, region, request))
