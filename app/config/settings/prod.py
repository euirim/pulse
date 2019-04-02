import os

from .base import *

DEBUG = False

ALLOWED_HOSTS = ['localhost', os.environ['HOST_IP'], '.euirim.org']

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


# Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'online@chicagomaroon.com'
EMAIL_HOST_PASSWORD = os.environ['PULSE_ADMIN_EMAIL_PASSWORD']
EMAIL_PORT = 587


CORS_ORIGIN_WHITELIST = (
    'euirim.org',
    'projects.euirim.org',
    'localhost',
    'localhost:3000',
    'localhost:8000',
    'projects.euirim.org.s3-website.us-east-2.amazonaws.com',
)