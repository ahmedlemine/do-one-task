from .base import *
from .base import INSTALLED_APPS
from .base import env

DEBUG = False
ALLOWED_HOSTS = ["localhost"]

INSTALLED_APPS = [
    # <insert apps for production only>,
    *INSTALLED_APPS
]

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["example.com"])
