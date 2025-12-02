from minio import Minio
from config import Config


USERNAME = Config.MINIO_ACCESS_KEY
PASSWORD = Config.MINIO_SECRET_KEY
URL = Config.MINIO_URL
DEFAULT_BUCKET = Config.MINIO_DEFAULT_BUCKET

class MinioConnector(object):
    pass