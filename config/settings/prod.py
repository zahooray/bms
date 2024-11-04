import os

from .base import *  # noqa
from .s3 import *  # noqa


DEBUG = False
ENABLE_DEBUG_TOOLS = False

INSTALLED_APPS += [  # noqa
    "storages",
]

STATIC_URL = "/django-static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")  # noqa

MEDIA_ROOT = os.path.join(BASE_DIR, "media")  # noqa
MEDIA_URL = f"https://{AWS_S3_ENDPOINT_URL}/{AWS_MEDIA_FILES_LOCATION}/"  # noqa

USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
