from django.conf import settings
from django.http import HttpResponseRedirect


def home_redirect(request):
    version_slug = settings.LOCALE_LATEST_VERSION_SLUG.get(
        request.LANGUAGE_CODE)
    if version_slug:
        return HttpResponseRedirect(version_slug + '/')
    return HttpResponseRedirect(
        '/{}/{}/'.format('en', settings.LOCALE_LATEST_VERSION_SLUG['en']))
