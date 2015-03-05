from django.conf import settings
from django.http import HttpResponseRedirect


def home_redirect(request):
    version = settings.LOCALE_LATEST_VERSION.get(request.LANGUAGE_CODE)
    if not version and settings.ENABLE_ALL_LANGUAGES:
        version = settings.LOCALE_LATEST_PENDING_VERSION.get(
            request.LANGUAGE_CODE)
    if version:
        return HttpResponseRedirect(version['slug'] + '/')
    return HttpResponseRedirect(
        '/{}/{}/'.format('en', settings.LOCALE_LATEST_VERSION['en']['slug']))
