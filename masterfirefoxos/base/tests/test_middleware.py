from django.http import HttpResponseRedirect
from django.test import RequestFactory
from django.test.utils import override_settings
from django.contrib.auth.models import AnonymousUser, User

from masterfirefoxos.base.tests import TEST_VERSIONS_LOCALE_MAP
from masterfirefoxos.base.middleware import NonExistentLocaleRedirectionMiddleware


middleware = NonExistentLocaleRedirectionMiddleware()


def test_user_authenticated():
    request = RequestFactory().get('/en/foo-bar')
    request.user = User()
    assert middleware.process_request(request) is None


def test_path_starts_with_en():
    request = RequestFactory().get('/en/foo-bar')
    request.user = AnonymousUser()
    assert middleware.process_request(request) is None


@override_settings(VERSIONS_LOCALE_MAP=TEST_VERSIONS_LOCALE_MAP)
def test_locale_for_version_exists():
    request = RequestFactory().get('/xx/version-90')
    request.user = AnonymousUser()
    assert middleware.process_request(request) is None


@override_settings(VERSIONS_LOCALE_MAP=TEST_VERSIONS_LOCALE_MAP)
def test_locale_for_version_does_not_exist():
    request = RequestFactory().get('/xx/version-100t/demo-tips')
    request.user = AnonymousUser()
    response = middleware.process_request(request)
    assert isinstance(response, HttpResponseRedirect)
    assert response.url == '/en/version-100t/demo-tips?from-lang=xx'


@override_settings(VERSIONS_LOCALE_MAP=TEST_VERSIONS_LOCALE_MAP)
def test_with_nonexistant_version():
    request = RequestFactory().get('/xx/version-does-not-exist/demo-tips')
    request.user = AnonymousUser()
    assert middleware.process_request(request) is None


def test_with_nonexistant_locale():
    request = RequestFactory().get('/xx/version-100t/demo-tips')
    request.user = AnonymousUser()
    assert middleware.process_request(request) is None


def test_request_path_breakdown_failure():
    request = RequestFactory().get('/')
    request.user = AnonymousUser()
    assert middleware.process_request(request) is None
