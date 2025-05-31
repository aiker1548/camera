# from botocore.client import BaseClient

# from infrastructure.data.file_storage.minio_s3.minio_storage import \
#     MinioStorageServiceImpl
# from shared_kernel.application.minio_storage import MinioStorageService


# class FileStorageUnitOfWorkImpl:
#     """ FileStorage implementation """

#     def __init__(self, s3_client: BaseClient, bucket_name: str):
#         self._s3_client = s3_client
#         self._bucket_name = bucket_name

#     @property
#     def file_storage_client(self) -> MinioStorageService:
#         return MinioStorageServiceImpl(s3_client=self._s3_client, bucket_name=self._bucket_name)
