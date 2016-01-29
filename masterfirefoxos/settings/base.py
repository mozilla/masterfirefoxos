"""
Django settings for masterfirefoxos project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

import os
from collections import OrderedDict

from django.utils.translation import ugettext_lazy as _

import dj_database_url
from decouple import Csv, config


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', cast=bool)


ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())

ENABLE_ALL_LANGUAGES = config('ENABLE_ALL_LANGUAGES', default=False, cast=bool)

# Application definition

INSTALLED_APPS = [
    # Third party apps
    'mptt',
    'feincms',
    'feincms.module.page',
    'feincms.module.medialibrary',
    'django_extensions',
    'django_stackato',
    'sorl.thumbnail',
    'storages',

    # Project specific apps
    'masterfirefoxos.base',

    # Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

for app in config('EXTRA_APPS', default='', cast=Csv()):
    INSTALLED_APPS.append(app)


MIDDLEWARE_CLASSES = (
    'django.middleware.cache.UpdateCacheMiddleware',
    'sslify.middleware.SSLifyMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'csp.middleware.CSPMiddleware',
    'masterfirefoxos.base.middleware.NonExistentLocaleRedirectionMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
)

ROOT_URLCONF = 'masterfirefoxos.urls'

WSGI_APPLICATION = 'masterfirefoxos.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': config(
        'DATABASE_URL',
        cast=dj_database_url.parse
    )
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = config('LANGUAGE_CODE', default='en-us')

TIME_ZONE = config('TIME_ZONE', default='UTC')

USE_I18N = config('USE_I18N', default=True, cast=bool)

USE_L10N = config('USE_L10N', default=True, cast=bool)

USE_TZ = config('USE_TZ', default=True, cast=bool)

STATIC_ROOT = config('STATIC_ROOT', default=os.path.join(BASE_DIR, 'static'))
STATIC_URL = config('STATIC_URL', '/static/')
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

MEDIA_ROOT = config('MEDIA_ROOT', default=os.path.join(BASE_DIR, 'media'))
MEDIA_URL = config('MEDIA_URL', '/media/')

SESSION_COOKIE_SECURE = config('SESSION_COOKIE_SECURE', default=not DEBUG, cast=bool)

# Django-CSP
CSP_DEFAULT_SRC = (
    "'self'",
    "https://*.youtube.com",
    "http://*.youtube.com",
    'https://pontoon.mozilla.org',
    'https://pontoon-dev.allizom.org',
)
CSP_FONT_SRC = (
    "'self'",
    'http://*.mozilla.net',
    'https://*.mozilla.net'
)
CSP_IMG_SRC = (
    "'self'",
    'http://*.mozilla.net',
    'https://*.mozilla.net',
    'https://ee-masterfirefoxos-dev.s3.amazonaws.com',
    'https://ee-masterfirefoxos-prod.s3.amazonaws.com',
    'https://pontoon.mozilla.org',
    'https://pontoon-dev.allizom.org',
    'http://www.google-analytics.com',
    'https://www.google-analytics.com',
)
CSP_SCRIPT_SRC = (
    "'self'",
    'http://www.mozilla.org',
    'https://www.mozilla.org',
    'http://*.mozilla.net',
    'https://*.mozilla.net',
    'https://pontoon.mozilla.org',
    'https://pontoon-dev.allizom.org',
    'http://www.google-analytics.com',
    'https://www.google-analytics.com',
)
CSP_STYLE_SRC = (
    "'self'",
    "'unsafe-inline'",
    'http://www.mozilla.org',
    'https://www.mozilla.org',
    'http://*.mozilla.net',
    'https://*.mozilla.net',
    'https://pontoon.mozilla.org',
    'https://pontoon-dev.allizom.org',
)

TEMPLATES = [
    {
        'BACKEND': 'django_jinja.backend.Jinja2',
        'APP_DIRS': True,
        'OPTIONS': {
            'match_extension': '.jinja',
            'newstyle_gettext': True,
            'context_processors': [
                'session_csrf.context_processor',
                'masterfirefoxos.base.context_processors.l18n',
                'masterfirefoxos.base.context_processors.settings',
            ],
        }
    },
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'session_csrf.context_processor',
            ],
        }
    },
]


LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

LANGUAGES = (
    ('af', _('Afrikaans')),
    ('ar', _('Arabic')),
    ('bn-bd', _('Bengali (Bangladesh)')),
    ('bn-in', _('Bengali (India)')),
    ('hr', _('Croatian')),
    ('cs', _('Czech')),
    ('ee', _('Ewe')),
    ('en', _('English')),
    ('de', _('German')),
    ('el', _('Greek')),
    ('ff', _('Fulah')),
    ('fr', _('French')),
    ('ha', _('Hausa')),
    ('hi-in', _('Hindi')),
    ('hu', _('Hungarian')),
    ('ig', _('Igbo')),
    ('it', _('Italian')),
    ('ja', _('Japanese')),
    ('ln', _('Lingala')),
    ('pl', _('Polish')),
    ('pt-br', _('Portuguese')),
    ('ro', _('Romanian')),
    ('ru', _('Russian')),
    ('sr', _('Serbian')),
    ('sw', _('Kiswahili')),
    ('es', _('Spanish')),
    ('ta', _('Tamil')),
    ('wo', _('Wolof')),
    ('xh', _('Xhosa')),
    ('xx', _('Pirate')),
    ('yo', _('Yoruba')),
    ('zu', _('Zulu')),
)
LANGUAGE_NAMES = dict(LANGUAGES)

VERSIONS_LOCALE_MAP = OrderedDict()
VERSIONS_LOCALE_MAP['1.1'] = {
    'slug': '1-1',
    'locales': ['cs', 'el', 'en', 'es', 'it', 'pt-br'],
    'pending_locales': [
        'hr', 'de', 'hu', 'pl', 'sr', 'xx']}
VERSIONS_LOCALE_MAP['1.3'] = {
    'slug': '1-3',
    'locales': ['en', 'es', 'cs'],
    'pending_locales': ['xx']}
VERSIONS_LOCALE_MAP['1.3T'] = {
    'slug': '1-3T',
    'locales': ['en', 'ta'],
    'pending_locales': ['hi-in', 'xx']}
VERSIONS_LOCALE_MAP['1.4'] = {
    'slug': '1-4',
    'locales': ['en', 'bn-in', 'ta', 'bn-bd'],
    'pending_locales': ['hi-in', 'xx']}
VERSIONS_LOCALE_MAP['2.0'] = {
    'slug': '2-0',
    'locales': [
        'af', 'ar', 'en', 'es', 'de', 'ff', 'fr', 'ja', 'pt-br', 'ro', 'sw',
        'wo', 'xh', 'zu'],
    'pending_locales': [
        'cs', 'ee', 'ha', 'hu', 'ig', 'ln',
        'pl', 'ru', 'xx', 'yo']}
VERSIONS_LOCALE_MAP['2.1'] = {
    'slug': '2-1',
    'locales': ['en', 'es'],
    'pending_locales': ['xx']}

LOCALE_LATEST_VERSION = {}
LOCALE_LATEST_PENDING_VERSION = {}
for name, version in VERSIONS_LOCALE_MAP.items():
    for locale in version['locales']:
        LOCALE_LATEST_VERSION[locale] = {
            'slug': version['slug'],
            'name': name,
            }
    for locale in version.get('pending_locales', []):
        LOCALE_LATEST_PENDING_VERSION[locale] = {
            'slug': version['slug'],
            'name': name,
            }

SSLIFY_DISABLE = config('DISABLE_SSL', default=DEBUG, cast=bool)
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True

AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID', default='')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY', default='')
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME', default='')

if AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY and AWS_STORAGE_BUCKET_NAME:
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

MIGRATION_MODULES = {
    'medialibrary': 'masterfirefoxos.base.migrate.medialibrary',
    'page': 'masterfirefoxos.base.migrate.page',
}


def media_files_unique_path(instance, filename):
    import os
    import uuid
    filename, ext = os.path.splitext(filename)
    return 'medialibrary/{}.{}{}'.format(filename, uuid.uuid4(), ext)


FEINCMS_MEDIALIBRARY_UPLOAD_TO = media_files_unique_path


THUMBNAIL_PRESERVE_FORMAT = True

LOCALIZATION_HOST = config('LOCALIZATION_HOST', default=None)

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}
if not DEBUG:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'unique-snowflake'
        }
    }

LOCALIZED_YOUTUBE_ID = {
    # 1.1
    'ODCBbEbcCGM': {
        'hr': 'QcDS5tfALy4',
        'de': 'zu2a0FXVh8c',
        'cs': 'v1tLRWtCkEs',
        'el': 'B9fwnibymws',
        'it': '9U6qXAqx9qw',
        'pl': 'IUfYEg2FGn4',
        'pt-br': '6mUYqNted2U',
        'sr': '-8-yc1KUBMs',
        'es': 'whcfcevIexg'
    },
    'SijuLONPI9U': {
        'hr': 'Ha3TerLNPQI',
        'de': '9bNfgtMa-H0',
        'cs': 'EBM2J9U6u1E',
        'el': 'dBYWqVOxf8Q',
        'it': 'cBUADOIP4ks',
        'pl': 'XYfESrBUkK8',
        'pt-br': 'wXlmBxaoLi8',
        'sr': 'Wur2jVusiDI',
        'es': 'hRPXmLOx1-w'
    },
    '-2V-hbYu9WQ': {
        'hr': 'Jk26OjisREE',
        'de': '0HWsDe_xfsM',
        'cs': 'PNedT1D6BR0',
        'el': 'hcSxACM2Zoc',
        'it': '0PiFn-2byP0',
        'pl': 'R3yT3mLzW3E',
        'pt-br': 'PCekhjtIxcs',
        'sr': 'TM9BUmlD6co',
        'es': 'ZrXfURfNK18'
    },
    'Dvne9wMwV6E': {
        'hr': 'Lc5AmjbdA-8',
        'de': 'c7t5vc16sck',
        'cs': '6jSEGncQTs4',
        'el': 'nkaAYhpvJ6o',
        'it': '-qmurnSReFE',
        'pl': 'DFQUPO2Zbr4',
        'pt-br': 'WGdJ_cL3LNc',
        'sr': 'dv4O2ju1vpA',
        'es': 'rMX9JtfYoBg'
    },
    '46dngYXUcFg': {
        'hr': 'wPX9GTkMj8E',
        'de': 'LXCZrsX0DRc',
        'cs': 'OAIWl4ZU-Fs',
        'el': 'JGCQ6lsOEO4',
        'it': 'Xqkgb6-CHpM',
        'pl': 'lodw2TvOOgU',
        'pt-br': 'zivYtU2lip0',
        'sr': 'Y04bxc3kVgE',
        'es': 'RhOLzXfqeBw'
    },
    'nwAUQvNuyTw': {
        'hr': '1fzu0Lf2XLo',
        'de': 'JNVcmXmkF5M',
        'cs': 'GoCINKDdAA0',
        'el': 'J--N_B5_Grk',
        'it': 'Oe9was4FQHA',
        'pl': 'jxN8ETP1c84',
        'pt-br': 'g7xGYUl_Odc',
        'sr': 'c0XSya6I39M',
        'es': 'kAvoXC0XkPw'
    },
    'ikbujo0l7dI': {
        'hr': 'oZazouOvw8s',
        'de': '5HnQ6o9HTns',
        'cs': 'X2zr6dITLWo',
        'el': 'ZmL0pLwhqqQ',
        'it': 'CsnZIFzdoNM',
        'pl': 'oU6bX-blsVo',
        'pt-br': 'c_A92GmAN94',
        'sr': 'XRawOINb-1k',
        'es': 'N89xDJyG15E'
    },
    'kGb4OLORKPA': {
        'hr': 'aH6y26VxnlM',
        'de': 'pRTWg1Yv_ko',
        'cs': 'hEluAdC02mI',
        'el': 'g8k8MjX9ZjM',
        'it': 'Z8ELi8wBR7o',
        'pl': 'vE1MxioVBBM',
        'pt-br': 'gqwl1xiLEkg',
        'sr': 'XDwIdH4hrgI',
        'es': 'mzOLVnujiJ0'
    },
    # 1.3
    'quZk7KJ68g0': {
        'es': 'c2UtgrpXRGc'
    },
    '7EruFl-AIRU': {
        'es': 'YHbzjfRrCDk'
    },
    'elW8ZT2shJY': {
        'es': '-CfZ5BK2Vik'
    },
    '1fGYn_Wfzp0': {
        'es': 'FG3tAR1GI58'
    },
    # 1.3T
    'yPRIgHARJsA': {
        'hi': 'akv0ylpKGbk',
        'ta': 'vcSts5T-va4'
    },
    'eBDX7k0gkJg': {
        'hi': 'zNGaHn3dSm4',
        'ta': 'TrjhifzgXso'
    },
    't_yNwJDAgKw': {
        'hi': 's64Wtw4e_8o',
        'ta': 'UGJo0wcU2cM'
    },
    'YarD9ZluQJU': {
        'hi': 'G5m4e0BR0JA',
        'ta': 'ityctnM6VEQ'
    },
    'hGvNjO82y-4': {
        'hi': 'rSOC6IAxyPk',
        'ta': 'YjEAgE3IGdo'
    },
    # 2.0
    '9WWo33tWwNw': {
        'ar': 'gjyt_fyNN10',
        'de': 'gfHbcpi3Rc4',
        'es': 'dBOY2I8jbNw',
        'fr': 'DPCDIkF9dN0',
        'pt-br': 'sJaHzQxiBY4',
        'ro': 'rhodrH2_xFg',
    },
    'jrcmZMkgHVU': {
        'ar': 'JJEZ0wWeFBs',
        'de': '_8dCK2zPAbA',
        'es': 'izI5jEUoyzE',
        'fr': 'RMnt-nfmytY',
        'pt-br': 'gAUfzgevRrw',
        'ro': 'pywAnwaK6nQ',
    },
    'i0UY48l-nXU': {
        'ar': 'K9lGP-l6RM8',
        'de': '5VlR0J3pMKg',
        'es': 'JeLDCekefps',
        'fr': 'gAsGJkBWtKo',
        'pt-br': 'nR0IcH4PKWs',
        'ro': 'bNmqAcl1-FY',
    },
    'blOcJrnirn0': {
        'ar': '7l5uZoLmkBo',
        'de': 'Z6aBrtRgTqQ',
        'es': '-5rUB-HPT-g',
        'fr': 'oVVV6qYlNEA',
        'pt-br': 'beML24YmXVo',
        'ro': '7a7cyt3L3WI',
    },
    '6ybgSsGZZU4': {
        'ar': 'HSlE-hv9PEw',
        'de': 'irGl0DmNgmo',
        'es': 'X-HPLiHHzUw',
        'fr': 'IZ9CnX38ai8',
        'pt-br': 'kfO2Vi9Jq_o',
        'ro': 'Q_56nl-n_6U',
    },
    'g5heblzMevA': {
        'ar': '4JAIXzfB0_o',
        'de': 'awg7mT-edwM',
        'es': 'zZ7Xvxc1Ta8',
        'fr': 'I3zYgwRzvVM',
        'pt-br': 'lR8Ql_bxoZ4',
        'ro': 'AkN2VtX7E-k',
    },
    # 2.1
    'WHn5K8sfJcI': {
        'es': 'TFaeqt27ZFc',
    },
    '763ieP4fFLg': {
        'es': 'YUk0M4FXVNQ',
    },
    'VyCVB9c5KdI': {
        'es': 'BCihTr2ZMxA',
    },
    'mPR3oi8jjRI': {
        'es': 'fK3VqHG4RiU',
    },
}
