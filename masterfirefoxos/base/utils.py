import os
from itertools import chain

from django.conf import settings
from feincms.module.page.models import Page


def entry_strings(entry):
    return [getattr(entry, field.name) for field in entry._meta.fields
            if field.name in getattr(entry, '_l10n_fields', [])]


def page_template_generator(page):
    yield '{% comment %}\n  Translators:'
    yield '    Page Title: ' + page.title
    if page.parent:
        yield '    Parent Page Title: ' + page.parent.title
    yield '{% endcomment %}'

    yield '{% blocktrans %}' + page.title + '{% endblocktrans %}'
    for content_type in page._feincms_content_types:
        for entry in page.content.all_of_type(content_type):
            for entry_string in entry_strings(entry):
                yield '\n'.join(['{% blocktrans trimmed %}', entry_string,
                                 '{% endblocktrans %}'])
    yield '\n'


def pages_l10n_template(pages=None):
    return '\n'.join(
        chain(*[page_template_generator(page) for page in
                pages or Page.objects.all()]))
