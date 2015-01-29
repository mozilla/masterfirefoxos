from unittest.mock import patch

from . import MediaFileFactory, ImageFieldFactory
from ..helpers import get_image_url


def test_get_image_url_base():
    with patch('masterfirefoxos.base.helpers.MediaFile') as MediaFileMock:
        MediaFileMock.objects.filter().exists.return_value = False
        media_file = MediaFileFactory()
        url = get_image_url(media_file)
    assert url == 'media_url'


def test_get_image_url_geometry():
    with patch('masterfirefoxos.base.helpers.MediaFile') as MediaFileMock:
        with patch('masterfirefoxos.base.helpers.get_thumbnail') as get_thumbnail_mock:
            MediaFileMock.objects.filter().exists.return_value = False
            media_file = MediaFileFactory()
            new_media_file = ImageFieldFactory(url='new_media_url')
            get_thumbnail_mock.return_value = new_media_file
            url = get_image_url(media_file, geometry='200')
    get_thumbnail_mock.assert_called_with(media_file.file, '200', quality=90)
    assert url == 'new_media_url'


def test_get_image_url_localized_file_exists():
    with patch('masterfirefoxos.base.helpers.MediaFile') as MediaFileMock:
        media_file = MediaFileFactory()
        localized_media_file = MediaFileFactory(url='localized_url')
        MediaFileMock.objects.filter().exists.return_value = True
        MediaFileMock.objects.filter().first.return_value = localized_media_file
        url = get_image_url(media_file)
    assert url == 'localized_url'
