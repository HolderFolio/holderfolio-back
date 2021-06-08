# import dj_database_url
from .base import *
from .utils import get_secret
import firebase_admin
from firebase_admin import credentials, auth
# from firebase_admin import firestore


DEBUG = True

    
SECRET_KEY = get_secret("SECRET_KEY")

INTERNAL_IPS = [
    '127.0.0.1',
]

INSTALLED_APPS += (
    # 'debug_toolbar',
)

MIDDLEWARE += (
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
)

# INITIALIZE FIREBASE
cred = credentials.Certificate("fbkey.json")
firebase_admin.initialize_app(cred)

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
