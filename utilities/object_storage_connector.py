import os
import logging
from minio import Minio
from minio.commonconfig import REPLACE, CopySource

class ObjectStorage:
    def __init__(self):
        self.mc = Minio(
            os.environ.get("MINIO_URL"),
            access_key=os.environ.get("MINIO_ACCESS_KEY"),
            secret_key=os.environ.get("MINIO_SECRET_KEY"),
            secure=False)

    def save_object(self, bucket, object):
        temp_dir = os.environ.get("TEMP_DIRECTORY")
        temp_dir += "" if temp_dir.endswith("/") else "/" # make sure it has a trailing '/'
        dest_file = temp_dir + object
        self.mc.fget_object(bucket, object, dest_file)
        return dest_file
    
    def update_object_metadata(self, bucket, object, metadata):
        self.mc.copy_object(bucket, object, CopySource(bucket, object), metadata=metadata, metadata_directive=REPLACE)
        return
    
    def is_connected(self):
        try:
            if not self.mc.bucket_exists("fakedatalakebucket"):
                logging.info("Connected to object storage")
                return True
        except Exception as e:
            logging.critical("Cannot connect to object storage")
            logging.critical(e, exc_info=True)
            return False