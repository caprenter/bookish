"""
Django settings for bookish project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/

Uses django-environ to get config from environment variables
https://github.com/joke2k/django-environ/
"""

import environ
root = environ.Path(__file__) - 2
env = environ.Env(DEBUG=(bool, False), SENTRY_DSN=(str, ''))  # set default values and casting

SITE_ROOT = root()

SECRET_KEY = env('SECRET_KEY')
DEBUG = env('DEBUG')

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

RAVEN_CONFIG = {
    'dsn': env('SENTRY_DSN')
}

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bookish',
    'fts',
    'raven.contrib.django.raven_compat',
    'debug_toolbar'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'bookish.urls'

WSGI_APPLICATION = 'bookish.wsgi.application'

DATABASES = {
    'default': env.db()
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-gb'

TIME_ZONE = 'Europe/London'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
