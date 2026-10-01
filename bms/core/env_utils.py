import os

from django.core.exceptions import ImproperlyConfigured


def get_env_variable(variable_name):
    try:
        return os.environ[variable_name]
    except KeyError:
        msg = f"Set the {variable_name} environment variable."
        raise ImproperlyConfigured(msg)


def get_env_file(file_path):
    if not os.path.exists(file_path):
        msg = f"Set the {file_path} environment file."
        raise ImproperlyConfigured(msg)

    return file_path
