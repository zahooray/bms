from project_name.core.env_utils import get_env_variable


AWS_ACCESS_KEY_ID = get_env_variable("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = get_env_variable("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = get_env_variable("AWS_STORAGE_BUCKET_NAME")
AWS_S3_ENDPOINT_URL = get_env_variable("AWS_S3_ENDPOINT_URL")
AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": "max-age=86400",
}
AWS_MEDIA_FILES_LOCATION = "media-files"
AWS_QUERYSTRING_EXPIRE = get_env_variable("AWS_QUERYSTRING_EXPIRE")
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
