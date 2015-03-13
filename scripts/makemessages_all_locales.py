from django.conf import settings
from django.core.management import call_command


def locale_dirname(locale):
    if '-' in locale:
        lang, country = locale.split('-')
        return '_'.join([lang, country.upper()])
    return locale


def run(*args):
    all_locales = [locale_dirname(locale) for locale, _ in settings.LANGUAGES]
    call_command('makemessages', locale=all_locales, keep_pot=True)
