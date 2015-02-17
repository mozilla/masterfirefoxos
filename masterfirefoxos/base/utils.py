from datetime import datetime
from itertools import chain

from django.db.models.fields import TextField
from django.utils.translation import ugettext as _

from feincms.module.page.models import Page


page_template_template = '''
{{% comment %}}
Translators:
    Page path: {parent_slug}/{page_slug}/
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
        page_slug=page.slug,
        parent_slug='/' + page.parent.slug if page.parent else '',
        string=page.title)

    for content_type in page._feincms_content_types:
        for entry in page.content.all_of_type(content_type):
            for entry_string in entry_strings(entry):
                yield page_template_template.format(
                    page_slug=page.slug,
                    parent_slug='/' + page.parent.slug if page.parent else '',
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


def youtube_embed_url(request, en_youtube_id):
    embed = 'https://www.youtube.com/embed/'
    youtube_id = _(en_youtube_id)
    if youtube_id == en_youtube_id and request and (
            not request.path.startswith('/en/')):
        query_template = '?hl={lang}&cc_lang_pref={lang}&cc_load_policy=1'
        lang = request.path.split('/')[1]  # validity ensured by middleware
        return embed + youtube_id + query_template.format(lang=lang)
    return embed + youtube_id


def unmangle(text):
    return text.replace(
        '\r\n', ' ').replace(
        '&rsquo;', '’').replace(
        '&ldquo;', '“').replace(
        '&rdquo;', '”').replace(
        '&mdash;', '—').replace(
        '<br />', '<br>').replace(
        '<p>&nbsp;</p>', '').replace(
        '<p>', '').replace(
        '</p>', '').replace(
        '<br><br>', ' ').replace(
        '<br>', ' ').strip()


def unmangle_pages(pages=None):
    for page in pages or Page.objects.all():
        for content_type in page._feincms_content_types:
            for entry in page.content.all_of_type(content_type):
                for field in entry._meta.fields:
                    if isinstance(field, TextField):
                        text = getattr(entry, field.name)
                        unmangled = unmangle(text)
                        if text != unmangled:
                            setattr(entry, field.name, unmangled)
                            entry.save(update_fields=[field.name])
