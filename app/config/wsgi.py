"""
WSGI config for pulse project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", 
    "config.settings.{}".format(os.environ["PULSE_HOST_TYPE"])
)

application = get_wsgi_application()
