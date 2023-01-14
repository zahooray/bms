import os

from .base import *  # noqa


DEBUG = False
ENABLE_DEBUG_TOOLS = False

STATIC_URL = "/django-static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")  # noqa

MEDIA_URL = "/django-media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")  # noqa
