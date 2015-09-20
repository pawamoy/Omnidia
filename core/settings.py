# -*- coding: utf-8 -*-

"""
Django settings for omnidia project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

from django.utils.translation import ugettext_lazy as _

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'se+a7o3pbl_-xz=+n9ra(*=s2*i4^e+t8kf2vnq@43v(#9=jaq'
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = True
ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = (
    'suit',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'watchdog',
    'rosetta',
    'django_extensions',
    'modeltranslation',
    'omnidia',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'core.urls'
WSGI_APPLICATION = 'core.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = False


gettext = lambda x: x
LANGUAGES = (
    ('en-us', gettext('English')),
    ('fr', gettext('French')),
)

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
MEDIA_URL = '/media/'
MEDIA_ROOT = '/media/pawantu/omnidia'
STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'omnidia-static')
ADMINS = (
    ('Timothée Mazzucotelli', 'timothee.mazzucotelli@gmail.com'),
)
TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)
APPEND_SLASH = True

# Context Processors
TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.i18n",
    "django.core.context_processors.request",
)

###############################################################################

# Django suit -----------------------------------------------------------------
SUIT_CONFIG = {
    'ADMIN_NAME': 'Django Suit',
    'SEARCH_URL': '/admin/auth/user/',
    'MENU': (
        # 'sites',
        {'label': _('Omnidia homepage'), 'icon': 'icon-home',
         'url': '/'},
        '-',
        {'app': 'auth', 'icon': 'icon-lock'},
        '-',
        {'label': _('General'), 'models': (
            'omnidia.dataset',
            'omnidia.datasetvalue',
            'omnidia.datatype',
        )},
        '-',
        {'label': _('Files'), 'models': (
            'omnidia.file',
            'omnidia.filetype',
        )},
        {'label': _('File fields'), 'models': (
            'omnidia.filedatasetfield',
            'omnidia.filespecificfield',
            'omnidia.fileglobalfield'
        )},
        {'label': _('File values'), 'models': (
            'omnidia.filedatasetvalue',
            'omnidia.filespecificvalue',
            'omnidia.fileglobalvalue'
        )},
        '-',
        {'label': _('Models'), 'models': (
            'omnidia.model',
            'omnidia.object',
            'omnidia.objectlink',
            'omnidia.objectfile',
            'omnidia.linkdata',
        )},
        {'label': _('Model fields'), 'models': (
            'omnidia.modeldatasetfield',
            'omnidia.modelspecificfield',
            'omnidia.modelglobalfield',
            'omnidia.modelglobaldatasetfield',
            'omnidia.modelmodelfield',
        )},
        {'label': _('Model values'), 'models': (
            'omnidia.modeldatasetvalue',
            'omnidia.modelspecificvalue',
            'omnidia.modelglobalvalue',
            'omnidia.modelglobaldatasetvalue',
            'omnidia.modelmodelvalue',
        )}
    ),
    # 'MENU_EXCLUDE': (
    #     'dataforms.collectiondataform',
    #     'dataforms.dataformfield',
    #     'dataforms.fieldchoice',
    #     'dataforms.answerchoice',
    # ),
    'LIST_PER_PAGE': 20
}
