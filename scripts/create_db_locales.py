from django.conf import settings

from masterfirefoxos.base.models import Locale


def run(*args):
    for code in settings.LANGUAGE_NAMES.keys():
            Locale.objects.get_or_create(code=code)
