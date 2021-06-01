# from .base import *
import dj_database_url
from .base import *
import os
import json
from django.core.exceptions import ImproperlyConfigured


DEBUG = True



with open("secret.json") as f:
    secret = json.loads(f.read())

def get_secret(secret_name, secrets=secret):
    try:
        return secrets[secret_name]
    except:
        msg = "La variable %s n'existe pas" % secret_name
        raise ImproperlyConfigured(msg)
    
SECRET_KEY = get_secret("SECRET_KEY")

INTERNAL_IPS = [
    '127.0.0.1',
]

INSTALLED_APPS += (
    'debug_toolbar',
)

MIDDLEWARE += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': get_secret("DB_NAME"),
        'USER': get_secret("USER"),
        'PASSWORD': get_secret("PASSWORD"),
        'HOST': 'localhost',
        'PORT': '',
    }
}
