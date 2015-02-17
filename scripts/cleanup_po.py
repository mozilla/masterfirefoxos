import re

from django.conf import settings

import polib


def code_string(occurrences):
    for occ in occurrences:
        if not occ[0].startswith('db-strings.txt'):
            return True
    return False


def valid_version(comment, versions):
    for version in versions:
        if re.search('Page path: /{}/'.format(re.escape(version)), comment):
            return True
    return False


def get_versions_for_locale(locale):
    versions = []
    for version, data in settings.VERSIONS_LOCALE_MAP.items():
        if (locale in data.get('locales', [])
            or locale in data.get('pending_locales', [])):
            versions.append(data['slug'])
    return versions


def run(*args):
    for locale, lang_name in settings.LANGUAGES:
        print('Processing locale {}'.format(locale))
        versions = get_versions_for_locale(locale)
        try:
            po = polib.pofile('locale/{}/LC_MESSAGES/django.po'.format(locale))
        except OSError:
            print('Cannot open po file for locale {}'.format(locale))
            continue

        to_remove = []
        for entry in po:
            # Currently unused string, keep.
            if len(entry.occurrences) == 0:
                continue

            # String that appears in code, keep.
            if code_string(entry.occurrences):
                continue

            # String from documenation version valid for locale, keep.
            if valid_version(entry.comment, versions):
                continue

            # Delete entry.
            to_remove.append(entry)

        for entry in to_remove:
            po.remove(entry)
        if to_remove:
            po.save()
