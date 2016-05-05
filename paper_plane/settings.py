# -*- coding: utf-8 -*-

"""
Django settings for paper_plane project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import k_util.set_default_encodeing
import os
import platform

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!


DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
TEMPLATE_ROOT = os.path.join(BASE_DIR, 'template/')


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'y4dj+z3kutjtc3x@-_qr-=5x#uc0$(^#%&7iesi$-+#evzvp$e'


# Application definition
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'account',
    'love_me',
    'lin',
    'subscription',
    'common',
    'mail_msg',
    'music_rss',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    # 'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'django.middleware.security.SecurityMiddleware',
)


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            TEMPLATE_ROOT,
            os.path.join(TEMPLATE_ROOT, 'love_me'),
            os.path.join(TEMPLATE_ROOT, 'service'),
            os.path.join(TEMPLATE_ROOT, 'lin'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


ROOT_URLCONF = 'paper_plane.urls'

WSGI_APPLICATION = 'paper_plane.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'paper_plane_db',
        'USER': 'root',
        'PASSWORD': 'tiankang',
        'HOST': '',
        'PORT': '',
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    },
}

import getpass

USER = getpass.getuser()

LOCAL_FLAG = True if USER == 'kangtian' else False
ENTRY_HOST = 'http://127.0.0.1:8000/' if LOCAL_FLAG else 'http://115.159.81.50/'

print 'The LOCAL_FLAG is %s' % LOCAL_FLAG

DB_DIR = '/data/db/'

SYSTEM = platform.system()
TEMP_DIR = '/tmp/paper_plane/'
if 'windows' in SYSTEM:
    TEMP_DIR = 'D:\\paper_plane\\temp\\'
else:
    TEMP_DIR = '/tmp/paper_plane/'

RES_DIR = '/data/res/'
if 'windows' in SYSTEM:
    TEMP_DIR = 'D:\\paper_plane\\res\\'
else:
    TEMP_DIR = '/tmp/paper_plane/'

IMAGE_RES = os.path.join(RES_DIR, 'img')


# STATICFILES_DIRS = [
#     STATIC_ROOT,
#     RES_DIR,
#     IMAGE_RES
# ]

from k_util.k_logger import log_inst


