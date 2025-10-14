from .base import *
from .base import INSTALLED_APPS

DEBUG = True

INSTALLED_APPS = [
    # <insert apps for dev only>,
    *INSTALLED_APPS
]


EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"