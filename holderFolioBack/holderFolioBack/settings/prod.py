from .base import *
from django.conf import settings

from .utils import get_env_variable

DEBUG = True

SECRET_KEY = get_env_variable('SECRET_KEY')

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', 
    }
}

INSTALLED_APPS += (
    'whitenoise.runserver_nostatic',
)

MIDDLEWARE += [
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

# Change 'default' database configuration with $DATABASE_URL.
DATABASES['default'] = dj_database_url.config()

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

django_heroku.settings(locals())
