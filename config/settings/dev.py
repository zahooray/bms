import os

from .base import *  # noqa


DEBUG = True
ENABLE_DEBUG_TOOLS = False

if ENABLE_DEBUG_TOOLS:
    INSTALLED_APPS += [  # noqa
        "debug_toolbar",
        "silk",
    ]

    MIDDLEWARE += [  # noqa
        "debug_toolbar.middleware.DebugToolbarMiddleware",
        "silk.middleware.SilkyMiddleware",
    ]

    INTERNAL_IPS = [
        "127.0.0.1",
    ]

    DEBUG_TOOLBAR_CONFIG = {"SHOW_TOOLBAR_CALLBACK": lambda _request: DEBUG}

STATIC_URL = "/django-static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")  # noqa

MEDIA_URL = "/django-media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")  # noqa
DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"
