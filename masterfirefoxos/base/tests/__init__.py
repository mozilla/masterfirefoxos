from collections import OrderedDict
from unittest.mock import Mock

from feincms.module.medialibrary.models import MediaFile
from sorl.thumbnail import ImageField


TEST_VERSIONS_LOCALE_MAP = OrderedDict({
    '9.0': {
        'slug': 'version-90',
        'locales': [
            'en',
            'xx',
            'foo',
        ]
    },
    '10.0t': {
        'slug': 'version-100t',
        'locales': [
            'en',
        ],
        'pending_locales': [
            'foo',
        ]
    }
})


def MediaFileFactory(filename='filename.jpg', url='media_url'):
    media_file = MediaFile()
    media_file.file = Mock()
    media_file.file.name = filename
    media_file.file.url = url
    return media_file


def ImageFieldFactory(filename='filename.jpg', url='image_url'):
    image_file = ImageField()
    image_file.name = filename
    image_file.url = url
    return image_file
