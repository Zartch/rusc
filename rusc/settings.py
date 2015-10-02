"""
Django settings for rusc project.
Generated by 'django-admin startproject' using Django 1.8.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '(s@g^td)*+n-jvnep_%q%fk23m!%9$kmepaw%u+mr*i6tb1g@8'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition



# Don't use the django-registration available from PyPI. It does not support Django 1.7 and it appears it never will. The repo maintainer has abdicated and the project appears unmaintained.
# There is a maintenance fork available on Github which has worked well for me with Django 1.7:
# https://github.com/macropin/django-registration
# It's available from PyPI as django-registration-redux.
# https://pypi.python.org/pypi/django-registration-redux/
# You can install using pip:
# pip install django-registration-redux
#FIQUEM EL NOM REGISTRATION PÈRO EN REALITAT FEM REFERENCIA AL DJANGO-REGISTRATION-REDUX COM ES POT VEURE A LES EXTERNAL LIBRARIES/DIST_PACKAGES, SI NO...PETA!

#TAMBE S'HA D'INSTALAR: 'autocomplete_light'  & 'notifications'


#django-messages esta obsolet respecte el django >1.7 pq en el urls.py utilitza una comanda "deprecated". per aixo copiem la api dins la nostra carpeta i la modifiquem

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_filters',
    'django_tables2',
    'django_messages',
    'notifications',
    'registration',
    'autocomplete_light',
    'post',
    'etiqueta',
    'recurs',
    'usuari',
    'buscador',
    'cela',
    'rusc.faq',


)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'rusc.urls'
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(PROJECT_ROOT, 'templates').replace('\\','/'),],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django_messages.context_processors.inbox',
                'rusc.context_processors.notifications_user',
                'cela.context_processors.cela_context',
                'rusc.context_processors.perfil_usuari'

            ],
        },
    },
]

WSGI_APPLICATION = 'rusc.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'


STATICFILES_DIRS = (os.path.join(BASE_DIR, 'rusc/static'),)
STATICFILES_DIRS = STATICFILES_DIRS

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'