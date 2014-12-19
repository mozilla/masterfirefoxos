from itertools import chain

from feincms.module.page.models import Page


page_template_template = '''
{{% comment %}}
Translators:
    Page Title: {title}
    Parent Page Title: {parent_title}
{{% endcoment %}}
{{% blocktrans trimmed %}}
{string}
{{% endblocktrans %}}
'''


def entry_strings(entry):
    return [getattr(entry, field.name) for field in entry._meta.fields
            if field.name in getattr(entry, '_l10n_fields', [])]


def page_template_generator(page):
    yield page_template_template.format(
        title=page.title,
        parent_title=page.parent and page.parent.title or 'None',
        string=page.title)

    for content_type in page._feincms_content_types:
        for entry in page.content.all_of_type(content_type):
            for entry_string in entry_strings(entry):
                yield page_template_template.format(
                    title=page.title,
                    parent_title=page.parent and page.parent.title or 'None',
                    string=entry_string)


def pages_l10n_template(pages=None):
    return '\n'.join(
        chain(*[page_template_generator(page) for page in
                pages or Page.objects.all()]))
