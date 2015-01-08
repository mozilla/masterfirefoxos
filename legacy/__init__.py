import json
import os

from django.conf import settings
from django.utils.text import slugify

from feincms.module.page.models import Page

import polib


def load_topic(language='english'):
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           'json', language + '.json')) as f:
        # all content for the legacy site is in a single 'topic'
        return json.load(f)['modules'][0]['topics'][0]


def add_richtext(page, text):
    if text:
        page.richtextentry_set.create(
            text=text, parent=page, region='main')


def add_blocks(page, blocks):
    for block in blocks or []:
        add_richtext(page, block['title'])
        for component in block['components']:
            add_richtext(page, component['title'])
            add_richtext(page, component['body'])
            # TODO: upload media, use different content type
            if component['component'] == 'graphic':
                add_richtext(page, component['graphic']['alt'])
            elif component['component'] in ('reveal', 'hotgraphic'):
                add_richtext(page, component['graphic']['title'])
                add_richtext(page, component['graphic'].get('body'))
            for item in component.get('items', []):
                add_richtext(page, item['title'])
                add_richtext(page, item.get('body'))
                add_richtext(page, item.get('strapline'))


def create_page(title, body='', parent=None, override_url='', blocks=None):
    page = Page.objects.create(
        title=title, slug=slugify(title), parent=parent,
        override_url=override_url)
    add_richtext(page, body)
    add_blocks(page, blocks)
    return page
    

def create_pages():
    topic = load_topic()
    home_page = create_page(topic['title'], topic['body'], override_url='/')
    for page in topic['pages']:
        create_page(page['title'], page.get('body'), parent=home_page,
                    blocks=page['articles'][0]['blocks'])


def update_if_present(source, translated, translations, keys):
    for key in keys:
        src = source.get(key)
        xlated = translated.get(key)
        if src and xlated:
            translations[src] = xlated


def update_component_translations(components, translated_components,
                                  translations):
    for component in components:
        for translated_component in translated_components:
            if translated_component['id'] == component['id']:
                update_if_present(component, translated_component, translations,
                                  ['title', 'body'])
                if component['component'] == 'graphic':
                    update_if_present(
                        component['graphic'], translated_component['graphic'],
                        translations, ['alt'])
                elif component['component'] in ('reveal', 'hotgraphic'):
                    update_if_present(
                        component['graphic'], translated_component['graphic'],
                        translations, ['title', 'body'])
                for item, translated_item in (
                        zip(component.get('items', []),
                            translated_component.get('items', []))):
                    update_if_present(
                        item, translated_item, translations,
                        ['title', 'body', 'strapline'])
                break


def update_block_translations(blocks, translated_blocks, translations):
    for block in blocks:
        for translated_block in translated_blocks:
            if translated_block['id'] == block['id']:
                update_if_present(block, translated_block,
                                  translations, ['title'])
            # component ids do not always match their parent block ids, so we
            # have to iterate through all the translated blocks
            update_component_translations(
                block['components'], translated_block['components'],
                translations)


def get_translations(language):
    topic = load_topic()
    translated_topic = load_topic(language)
    translations = {}

    for page in topic['pages']:
        for translated_page in translated_topic['pages']:
            if translated_page['id'] == page['id']:
                update_if_present(page, translated_page, translations,
                                  ['title', 'body'])
                update_block_translations(
                    page['articles'][0]['blocks'],
                    translated_page['articles'][0]['blocks'],
                    translations)
    return translations



def load_po(language):
    language_codes = {'german': 'de'}
    return polib.pofile(os.path.join(settings.BASE_DIR, 'locale',
                                     language_codes[language], 'LC_MESSAGES',
                                     'django.po'))


def update_po(language):
    translations = get_translations(language)
    po = load_po(language)
    translated = False
    for entry in po:
        translated = translations.get(entry.msgid)
        if translated:
            if entry.msgstr and entry.msgstr != translated:
                print('replacing', entry.msgstr, 'with', translated,
                      'for', entry.msgid)
            entry.msgstr = translated
    po.save()
