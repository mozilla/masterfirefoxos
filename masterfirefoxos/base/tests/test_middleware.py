from django.http import HttpResponseRedirect
from django.test import RequestFactory
from django.test.utils import override_settings

from masterfirefoxos.base.tests import TEST_VERSIONS_LOCALE_MAP
from masterfirefoxos.base.middleware import NonExistentLocaleRedirectionMiddleware


middleware = NonExistentLocaleRedirectionMiddleware()


def test_path_starts_with_en():
    request = RequestFactory().get('/en/foo-bar')
    assert middleware.process_request(request) is None


@override_settings(ENABLE_ALL_LANGUAGES=True)
def test_enable_all_languages():
    request = RequestFactory().get('/xx-dne/')
    assert middleware.process_request(request) is None


@override_settings(VERSIONS_LOCALE_MAP=TEST_VERSIONS_LOCALE_MAP,
                   ENABLE_ALL_LANGUAGES=False)
def test_locale_for_version_exists():
    request = RequestFactory().get('/xx/version-90')
    assert middleware.process_request(request) is None


@override_settings(VERSIONS_LOCALE_MAP=TEST_VERSIONS_LOCALE_MAP,
                   ENABLE_ALL_LANGUAGES=False)
def test_locale_for_version_does_not_exist():
    request = RequestFactory().get('/xx/version-100t/demo-tips')
    response = middleware.process_request(request)
    assert isinstance(response, HttpResponseRedirect)
    assert response.url == '/en/version-100t/demo-tips?from-lang=xx'


@override_settings(VERSIONS_LOCALE_MAP=TEST_VERSIONS_LOCALE_MAP,
                   ENABLE_ALL_LANGUAGES=False)
def test_with_nonexistant_version():
    request = RequestFactory().get('/xx/version-does-not-exist/demo-tips')
    assert middleware.process_request(request) is None


@override_settings(VERSIONS_LOCALE_MAP=TEST_VERSIONS_LOCALE_MAP,
                   ENABLE_ALL_LANGUAGES=False)
def test_request_path_breakdown_failure():
    request = RequestFactory().get('/')
    assert middleware.process_request(request) is None
