import os

from project_name.core.env_utils import get_env_variable

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

SENDGRID_ECHO_TO_STDOUT = True
SENDGRID_SANDBOX_MODE_IN_DEBUG = get_env_variable("SENDGRID_SANDBOX_MODE_IN_DEBUG") in ("True", "true", 1)
