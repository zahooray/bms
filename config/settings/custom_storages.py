import os

from tempfile import SpooledTemporaryFile

from storages.backends.s3boto3 import S3Boto3Storage  # noqa


class CustomS3Boto3Storage(S3Boto3Storage):
    """
    This is our custom version of S3Boto3Storage that fixes a bug in
    boto3 where the passed in file is closed upon upload.
    """

    def _save(self, name, content):
        # Seek our content back to the start
        content.seek(0, os.SEEK_SET)

        # Create a temporary file that will write to disk after a specified
        # size.
        # This file will be automatically deleted when closed by
        # boto3 or after exiting the `with` a statement if the boto3 is fixed
        with SpooledTemporaryFile() as content_autoclose:
            # Handle different types of content appropriately
            first_byte = content.read(1)
            content.seek(0, os.SEEK_SET)
            if isinstance(first_byte, str):
                # Text content
                read_content = content.read().encode("utf-8")
                content_autoclose.write(read_content)
            else:
                # Binary content
                content_autoclose.write(content.read())

            # Upload the object which will auto close the
            # content_auto close instance
            return super()._save(name, content_autoclose)  # noqa


class StaticStorage(S3Boto3Storage):
    location = "staticfiles"
    file_overwrite = False
