from .base import *


DEBUG = False


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'HOST': 'db',
        'PORT': 5432,
    }
}

# Static files
STATIC_ROOT = os.path.join(BASE_DIR, "../assets")


CORS_ORIGIN_WHITELIST = (
    'euirim.org',
    'localhost',
    'localhost:3000'
)