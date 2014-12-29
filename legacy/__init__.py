import json
import os

from django.utils.text import slugify

from feincms.module.page.models import Page


def load(language='english'):
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           'json', '{}.json'.format(language))) as f:
        return json.load(f)


def add_richtext(page, text):
    if text:
        page.richtextentry_set.create(
            text='<p>{}</p>'.format(text), parent=page, region='main')


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
    # all content for the legacy site is in a single 'topic'
    topic = load()['modules'][0]['topics'][0]
    home_page = create_page(topic['title'], topic['body'], override_url='/')
    for page in topic['pages']:
        create_page(page['title'], page.get('body'), parent=home_page,
                    blocks=page['articles'][0]['blocks'])
