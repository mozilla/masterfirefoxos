from datetime import datetime
from itertools import chain

from feincms.module.page.models import Page


page_template_template = '''
{{% comment %}}
Translators:
    Page Title: {title}
    Parent Page Title: {parent_title}
{{% endcomment %}}
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


def copy_content_and_children(page, new_page):
    new_page.copy_content_from(page)
    for child in page.get_children():
        copy_page_with_parent(child, new_page)
    return new_page


def copy_page_with_parent(page, parent):
    new_page = Page.objects.create(
        title=page.title, slug=page.slug, parent=parent, active=False)
    return copy_content_and_children(page, new_page)


def copy_tree(page):
    now = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    new_page = Page.objects.create(
        title='Copy of {title} on {now}'.format(title=page.title, now=now),
        slug='copy-of-{slug}-on-{now}'.format(slug=page.slug, now=now),
        parent=page.parent, active=False)
    return copy_content_and_children(page, new_page)
