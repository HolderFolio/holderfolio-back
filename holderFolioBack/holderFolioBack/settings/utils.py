import os
from django.core.exceptions import ImproperlyConfigured

def get_env_variable(var_nam,default_value=None):
    try:
        return os.environ[var_nam]
    except keyError:
        if default_value is None:
            msg = "La variable %s n'existe pas" % var_nam
            raise ImproperlyConfigured(msg) 
        else:
            return default_value
            
        
    