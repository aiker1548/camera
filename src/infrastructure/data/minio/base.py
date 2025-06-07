from src.shared_kernel.config import config
from minio import Minio

minio_client = Minio(
        endpoint=config.MINIO_ENDPOINT,
        access_key=config.MINIO_ACCESS_KEY,
        secret_key=config.MINIO_SECRET_KEY,
        secure=config.MINIO_SECURE
        )

def get_minio_client():
    video_bucket = config.MINIO_VIDEO_BUCKET
    preview_bucket = config.MINIO_PREVIEW_BUCKET
    if not minio_client.bucket_exists(video_bucket):
        minio_client.make_bucket(video_bucket)
    if not minio_client.bucket_exists(preview_bucket):
        minio_client.make_bucket(preview_bucket)
    return minio_client