import os
from django.core.exceptions import ImproperlyConfigured
import json


def get_env_variable(var_nam,default_value=None):
    try:
        return os.environ[var_nam]
    except keyError:
        if default_value is None:
            msg = "La variable %s n'existe pas" % var_nam
            raise ImproperlyConfigured(msg) 
        else:
            return default_value

with open("secret.json") as f:
    secret = json.loads(f.read())

def get_secret(secret_name, secrets=secret):
    try:
        return secrets[secret_name]
    except:
        msg = "La variable %s n'existe pas" % secret_name
        raise ImproperlyConfigured(msg)
        
    