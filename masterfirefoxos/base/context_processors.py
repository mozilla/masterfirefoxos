from django.conf import settings as django_settings
from django.utils import translation


def l18n(request):
    return {
        'LANG': translation.get_language(),
        'DIR': 'rtl' if translation.get_language_bidi() else 'ltr',
    }


def settings(request):
    return {
        'settings': django_settings,
    }
