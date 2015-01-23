from django.test import RequestFactory
from django.test.utils import override_settings

from .. import views


@override_settings(
    LOCALE_LATEST_VERSION={
        'de': {'slug': '1-1', 'name': '1.1'},
        'en': {'slug': '1-3T', 'name': '1.3T'}
    })
def test_home_redirect_de():
    request = RequestFactory().get('/de/')
    request.LANGUAGE_CODE = 'de'  # normally added by LocaleMiddleware
    response = views.home_redirect(request)
    assert response.status_code == 302
    assert response['location'] == '1-1/'


@override_settings(LOCALE_LATEST_VERSION={'en': {'slug': '1-3T', 'name': '1.3T'}})
def test_home_redirect_english_default():
    request = RequestFactory().get('/de/')
    request.LANGUAGE_CODE = 'de'  # normally added by LocaleMiddleware
    response = views.home_redirect(request)
    assert response.status_code == 302
    assert response['location'] == '/en/1-3T/'
