from django.apps import AppConfig

from .models import Page


class BaseAppConfig(AppConfig):
    name = 'masterfirefoxos.base'

    def ready(self):
        Page.__str__ = lambda x: x.slug
