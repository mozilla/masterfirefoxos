from django.conf import settings


def settings(request):
    return {
        'settings': settings
    }
