from collections import defaultdict
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


def strip_po_ptags(locale):
    po = load_po(locale)
    for entry in po:
        entry.msgid = punwrap(entry.msgid)
        entry.msgstr = punwrap(entry.msgstr)
    po.save()


def dedupe_po(locale):
    msgid_entries = defaultdict(list)
    po = load_po(locale)
    for entry in po:
        msgid_entries[entry.msgid].append(entry)
    dupes_to_remove = []
    for msgid, entries in msgid_entries.items():
        if len(entries) > 1:
            if entries[0].msgstr and entries[0].comment and (
                    not entries[0].obsolete) or not any(
                        e.msgstr for e in entries):
                dupes_to_remove.extend(entries[1:])
            elif entries[1].msgstr and entries[1].comment and (
                    not entries[1].obsolete):
                dupes_to_remove.append(entries[0])
            else:
                print('Unable to automatically resolve dupes in {} for:'.format(
                      locale))
                print(msgid)
    for dupe in dupes_to_remove:
        po.remove(dupe)
    po.save()


def strip_extraneous_newlines(locale):
    po = load_po(locale)
    extraneous_newlines = False
    for entry in po:
        if '\n' in entry.msgstr and '\n' not in entry.msgid:
            entry.msgstr = entry.msgstr.replace('\n', '')
            extraneous_newlines = True
    if extraneous_newlines:
        po.save()
        print('Fixed extraneous newlines in ' + locale)


def split_h2(text):
    h2, text = text.split('</h2>', 1)
    return h2.replace('<h2>', ''), text


def split_po_h2s(locale):
    po = load_po(locale)
    to_split = [
        entry for entry in po
        if entry.msgid.startswith('<h2>') and '</h2>' in entry.msgid
        and entry.msgstr.startswith('<h2>') and '</h2>' in entry.msgstr]
    for entry in to_split:
        h2, text = split_h2(entry.msgid)
        translated_h2, translated_text = split_h2(entry.msgstr)
        if h2 and text and translated_h2 and translated_text:
            h2_entry = polib.POEntry()
            h2_entry.msgid = h2
            h2_entry.msgstr = translated_h2
            h2_entry.comment = entry.comment
            index = po.index(entry)
            po.insert(index, h2_entry)
            text_entry = polib.POEntry()
            text_entry.msgid = text
            text_entry.msgstr = translated_text
            text_entry.comment = entry.comment
            po.insert(index + 1, text_entry)
            po.remove(entry)
    po.save()


def split_h3(text):
    # assumes <h3> at end of text
    text, h3 = text.split('<h3>', 1)
    return h3.replace('</h3>', ''), text


def split_po_h3s(locale):
    po = load_po(locale)
    to_split = [
        entry for entry in po
        if entry.msgid.endswith('</h3>') and '<h3>' in entry.msgid
        and entry.msgstr.endswith('</h3>') and '<h3>' in entry.msgstr]
    for entry in to_split:
        h3, text = split_h3(entry.msgid)
        translated_h3, translated_text = split_h3(entry.msgstr)
        if h3 and text and translated_h3 and translated_text:
            h3_entry = polib.POEntry()
            h3_entry.msgid = h3
            h3_entry.msgstr = translated_h3
            h3_entry.comment = entry.comment
            index = po.index(entry)
            po.insert(index, h3_entry)
            text_entry = polib.POEntry()
            text_entry.msgid = text
            text_entry.msgstr = translated_text
            text_entry.comment = entry.comment
            po.insert(index + 1, text_entry)
            po.remove(entry)
    po.save()


def fix_all_locales():
    for locale, language in settings.LANGUAGES:
        if locale != 'en':
            strip_po_ptags(locale)
            split_po_h2s(locale)
            split_po_h3s(locale)
            dedupe_po(locale)
            strip_extraneous_newlines(locale)


def save_h2_to_next_entry(entry):
    found = False
    for e in entry.parent.richtextentry_set.all():
        if e == entry:
            found = True
        elif found:
            e.subheader_2 = entry.subheader_2
            e.save(update_fields='subheader_2')
            break
    return found


def save_h3_to_next_entry(entry):
    found = False
    for e in entry.parent.richtextentry_set.all():
        if e == entry:
            found = True
        elif found:
            e.subheader_3 = entry.subheader_3
            e.save(update_fields=['subheader_3'])
            break
    return found


def split_db_h2s():
    page = Page.objects.all()[0]
    to_delete = []
    for entry in page.richtextentry_set.model.objects.filter(
            text__startswith='<h2>'):
        if '</h2>' not in entry.text:
            print('Missing </h2> in RichTextEntry {} on {}'.format(
                  entry.text, entry.parent.get_absolute_url()))
            continue
        entry.subheader_2, entry.text = split_h2(entry.text)
        if entry.text:
            entry.save(update_fields=['text', 'subheader_2'])
        elif save_h2_to_next_entry(entry):
            to_delete.append(entry)
    for entry in to_delete:
        entry.delete()


def split_db_h3s():
    page = Page.objects.all()[0]
    for entry in page.richtextentry_set.model.objects.filter(
            text__endswith='</h3>'):
        if '<h3>' not in entry.text:
            print('Missing <h3> in RichTextEntry {} on {}'.format(
                  entry.text, entry.parent.get_absolute_url()))
            continue
        entry.subheader_3, entry.text = split_h3(entry.text)
        if save_h3_to_next_entry(entry) and entry.text:
            entry.subheader_3 = ''
            entry.save(update_fields=['text'])
