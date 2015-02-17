from django.test.utils import override_settings

from masterfirefoxos.base.tests import TEST_VERSIONS_LOCALE_MAP
from cleanup_po import code_string, get_versions_for_locale, valid_version


def test_code_string():
    assert code_string([('foo', 2), ('bar', 3)]) is True
    assert code_string([('foo', 3), ('db-strings.txt', 10)]) is True
    assert code_string([('db-strings.txt', 10)]) is False


def test_valid_version():
    comment = 'FooBar\nPage path: /1-3T/foo/bar\nLalo'
    assert valid_version(comment, ['1-1', '1-3T']) is True
    assert valid_version(comment, ['2-0', '1-3']) is False


@override_settings(VERSIONS_LOCALE_MAP=TEST_VERSIONS_LOCALE_MAP)
def test_get_versions_for_locale():
    assert get_versions_for_locale('xx') == ['version-90']
    assert set(get_versions_for_locale('en')) == set(['version-90', 'version-100t'])
    assert set(get_versions_for_locale('foo')) == set(['version-90', 'version-100t'])
