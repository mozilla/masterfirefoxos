from unittest.mock import Mock

from django.http import HttpResponseRedirect
from django.test.utils import override_settings

from masterfirefoxos.base.tests import TEST_VERSIONS_LOCALE_MAP
from masterfirefoxos.base.middleware import NonExistentLocaleRedirectionMiddleware


middleware = NonExistentLocaleRedirectionMiddleware()


def test_user_authenticated():
    request = Mock()
    request.user.is_authenticated.return_value = True
    assert middleware.process_request(request) is None


def test_path_starts_with_en():
    request = Mock()
    request.user.is_authenticated.return_value = False
    request.path.startswith.return_value = '/en/foo-bar'
    assert middleware.process_request(request) is None


@override_settings(VERSIONS_LOCALE_MAP=TEST_VERSIONS_LOCALE_MAP)
def test_locale_for_version_exists():
    request = Mock()
    request.user.is_authenticated.return_value = False
    request.path = '/xx/version-90'
    assert middleware.process_request(request) is None


@override_settings(VERSIONS_LOCALE_MAP=TEST_VERSIONS_LOCALE_MAP)
def test_locale_for_version_does_not_exist():
    request = Mock()
    request.user.is_authenticated.return_value = False
    request.path = '/xx/version-100t/demo-tips'
    response = middleware.process_request(request)
    assert isinstance(response, HttpResponseRedirect)
    assert response.url == '/en/version-100t/demo-tips'


@override_settings(VERSIONS_LOCALE_MAP=TEST_VERSIONS_LOCALE_MAP)
def test_with_nonexistant_version():
    request = Mock()
    request.user.is_authenticated.return_value = False
    request.path = '/xx/version-does-not-exist/demo-tips'
    assert middleware.process_request(request) is None


def test_with_nonexistant_locale():
    request = Mock()
    request.user.is_authenticated.return_value = False
    request.path = '/xx/version-100t/demo-tips'
    assert middleware.process_request(request) is None


def test_request_path_breakdown_failure():
    request = Mock()
    request.user.is_authenticated.return_value = False
    request.path = '/'
    assert middleware.process_request(request) is None
