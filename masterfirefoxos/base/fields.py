from django.db import models


class LocalizableField(object):
    pass


class LocalizableCharField(models.CharField, LocalizableField):
    pass


class LocalizableTextField(models.TextField, LocalizableField):
    pass
