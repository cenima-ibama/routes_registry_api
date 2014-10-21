from .base import *

########## IN-MEMORY TEST DATABASE
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'router_test',
        'USER': 'casv',
        'PASSWORD': 'casv',
        'HOST': '',
        'PORT': '',
    }
}

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
)
