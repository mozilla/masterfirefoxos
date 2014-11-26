import os

from django.conf import settings

import cronjobs
from feincms.module.page.models import Page
from masterfirefoxos.base.fields import LocalizableField

EXPORT_TO = os.path.join(settings.BASE_DIR, 'db-strings.txt')

TEMPLATE = """{% comment %}
  Translators:
    Page Title: {{ title }}
    Parent Page Title: {{ parent_title }}
{% endcomment %}
{% blocktrans trimmed %}
  {{ value }}
{% endblocktrans %}

"""


@cronjobs.register
def extract_database_strings():
    with open(EXPORT_TO, 'w') as fp:
        for page in Page.objects.all():
            for content_type in page._feincms_content_types:
                for entry in page.content.all_of_type(content_type):
                    for field in entry._meta.fields:
                        if not isinstance(field, LocalizableField):
                            continue

                        context = {
                            '{{ title }}': page.title,
                            '{{ parent_title }}': page.parent.title if page.parent else 'None',
                            '{{ value }}': getattr(entry, field.name)
                        }
                        original = TEMPLATE
                        for key, value in context.items():
                            original = original.replace(key, value)
                        fp.write(original)
