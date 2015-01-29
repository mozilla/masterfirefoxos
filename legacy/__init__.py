from functools import lru_cache
import json
import os

from django.conf import settings
from django.core.management import call_command
from django.db import DataError
from django.utils.text import slugify

from feincms.module.page.models import Page

import polib


@lru_cache(maxsize=None)
def load_json(*args):
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           'json', *args)) as f:
        return json.load(f)


def load_topic(language='en', version='1.3T'):
    # all content for the legacy site is in a single 'topic'
    return load_json(
        version, language + '.json')['modules'][0]['topics'][0]


def video_path_to_youtube_id(video_path):
    return load_json('video_path_to_youtube_id.json').get(video_path)


def pwrap(text):
    if text.startswith('<p>') and text.endswith('</p>'):
        return text
    else:
        return '<p>{}</p>'.format(text)


def punwrap(text):
    return text.replace('<p>', '').replace('</p>', '')


def inc_ordering(page):
    page.ordering = getattr(page, 'ordering', 0) + 1
    return page.ordering


def add_richtext(page, text):
    if text:
        entry, created = page.richtextentry_set.get_or_create(
            text=pwrap(text), parent=page, region='main')
        if created:
            entry.ordering = inc_ordering(page)
            entry.save(update_fields=['ordering'])


def add_quiz_question_and_answers(page, component):
    page.quizquestion_set.create(
        question=component['body'],
        correct_feedback=component['feedback']['correct'],
        incorrect_feedback=component['feedback']['incorrect'],
        partly_correct_feedback=component['feedback']['partly'],
        parent=page, region='main', ordering=inc_ordering(page))
    for item in component['items']:
        page.quizanswer_set.create(
            answer=item['text'], correct=item['correct'],
            parent=page, region='main', ordering=inc_ordering(page))


def pop_page_text(page):
    entries = page.richtextentry_set.all()[:1]
    if entries:
        entry = entries[0]
        entry.delete()
        page.richtextentry_set.update()
        return punwrap(entry.text)
    return ''


def add_youtube_paragraph(page, component):
    youtube_id = video_path_to_youtube_id(
        component['media']['ogv']) or video_path_to_youtube_id(
        component['media']['mp4']) or 'MISSING'
    title = component['title'] or pop_page_text(page)
    text = component['body'] or pop_page_text(page)
    try:
        page.youtubeparagraphentry_set.create(
            title=title, text=text, youtube_id=youtube_id, parent=page,
            region='main')
    except DataError:  # swap text and title
        page.youtubeparagraphentry_set.create(
            title=text, text=title, youtube_id=youtube_id, parent=page,
            region='main')


def add_blocks(page, blocks):
    for block in blocks or []:
        add_richtext(page, block['title'])
        for component in block['components']:
            if component['component'] == 'mcq':
                add_quiz_question_and_answers(page, component)
            elif component['component'] == 'media':
                add_youtube_paragraph(page, component)
            elif component.get('class') not in ('nav-next', 'nav-back'):
                add_richtext(page, component['title'])
                add_richtext(page, component['body'])
                if component['component'] == 'graphic':
                    # TODO: upload media, use different content type
                    add_richtext(page, component['graphic']['alt'])
                elif component['component'] in ('reveal', 'hotgraphic'):
                    # TODO: upload media, use different content type
                    add_richtext(page, component['graphic']['title'])
                    add_richtext(page, component['graphic'].get('body'))
                for item in component.get('items', []):
                    add_richtext(page, item['title'])
                    add_richtext(page, item.get('body'))
                    add_richtext(page, item.get('strapline'))


def create_page(title, body='', parent=None, slug='', blocks=None):
    page = Page.objects.create(
        title=title, slug=slug or slugify(title), parent=parent)
    add_richtext(page, body)
    add_blocks(page, blocks)
    return page


def create_pages(version='1.3T'):
    topic = load_topic(version=version)
    home_page = create_page(topic['title'], topic['body'],
                            slug=version.replace('.', '-'))
    for page in topic['pages']:
        create_page(page['title'], page.get('body'), parent=home_page,
                    blocks=page['articles'][0]['blocks'])


def update_if_present(source, translated, translations, keys):
    for key in keys:
        src = source.get(key)
        xlated = translated.get(key)
        if src and xlated:
            translations[src] = xlated
            translations[pwrap(src)] = pwrap(xlated)


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


def get_translations(language, version):
    topic = load_topic(version=version)
    translated_topic = load_topic(language=language, version=version)
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
    return polib.pofile(os.path.join(settings.BASE_DIR, 'locale', language,
                                     'LC_MESSAGES', 'django.po'))


def update_po(language, version):
    translations = get_translations(language, version)
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


def create_pages_and_translations():
    for version, locale_map in settings.VERSIONS_LOCALE_MAP.items():
        create_pages(version=version)
        call_command('runscript', 'db_strings')
        for locale in locale_map['locales']:
            if locale == 'en':
                continue
            call_command('makemessages', locale=[locale])
            update_po(locale, version)
    call_command('compilemessages')
