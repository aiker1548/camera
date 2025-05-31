# from dataclasses import dataclass
# from typing import BinaryIO

# from botocore.client import BaseClient
# from botocore.exceptions import ClientError

# from shared_kernel.application.minio_storage import MinioStorageService


# @dataclass(frozen=True)
# class MinioStorageServiceImpl(MinioStorageService):
#     s3_client: BaseClient
#     bucket_name: str

#     def _upload_file(self, file_data: bytes, filename: str, additional_path: str = "") -> str:
#         try:
#             self.s3_client.head_bucket(Bucket=self.bucket_name)
#         except ClientError:
#             self.s3_client.create_bucket(Bucket=self.bucket_name)

#         file_path = f"{additional_path.rstrip('/')}/{filename}".lstrip("/")
#         self.s3_client.put_object(
#             Bucket=self.bucket_name,
#             Key=file_path,
#             Body=file_data
#         )
#         return file_path

#     def _generate_url(self, object_key: str, expiration: int = 1000) -> str:
#         presigned_url = self.s3_client.generate_presigned_url(
#             "get_object",
#             Params={
#                 "Bucket": self.bucket_name,
#                 "Key": object_key
#             },
#             ExpiresIn=expiration
#         )
#         return presigned_url

#     def _get_file(self, object_key: str) -> BinaryIO:
#         response = self.s3_client.get_object(Bucket=self.bucket_name, Key=object_key)
#         file_content = response["Body"].read()
#         return file_content

#     def _delete_file(self, object_key: str) -> None:
#         self.s3_client.delete_object(Bucket=self.bucket_name, Key=object_key)
