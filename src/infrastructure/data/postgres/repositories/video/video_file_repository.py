# import sqlalchemy as sa

# from application.video.interfaces.persistence.repo import VideoFileRepo
# from domain.value_objects.auth.user_id import UserId
# from domain.video.entities.video_file import VideoFile as VideoFileDomain
# from domain.video.value_objects.video_file import (DeletedAt, FileErrors,
#                                                    Filename, FileSize,
#                                                    FileStatus, UploadedAt)
# from infrastructure.data.postgres import models
# from infrastructure.data.postgres.base import SQLAlchemyRepo
# from infrastructure.data.postgres.converters import \
#     convert_video_file_entity_to_db_model
# from shared_kernel.building_blocks.domain.entity_id import EntityId


# class VideoFileRepositoryImpl(SQLAlchemyRepo, VideoFileRepo):
#     async def create(self, file: VideoFileDomain) -> None:
#         db_file = convert_video_file_entity_to_db_model(file)
#         self._session.add(db_file)
#         await self._session.flush((db_file,))

#     async def update(self, file: VideoFileDomain) -> None:
#         db_file = convert_video_file_entity_to_db_model(file)
#         await self._session.merge(db_file)
#         await self._session.flush()

#     async def _find_by_id(self, file_id: EntityId) -> VideoFileDomain | None:
#         result = await self._session.execute(
#             sa.select(models.VideoFile).filter(models.VideoFile.id == file_id.to_raw())
#         )
#         db_file = result.scalars().first()
#         return db_file and self._to_domain(db_file)

#     async def _delete(self, file_id: EntityId) -> None:
#         result = await self._session.execute(
#             sa.select(models.VideoFile).filter(models.VideoFile.id == file_id.to_raw())
#         )
#         db_file = result.scalars().first()

#         await self._session.delete(db_file)
#         await self._session.flush()

#     @staticmethod
#     def _to_domain(file_model: models.VideoFile) -> VideoFileDomain:
#         return VideoFileDomain(
#             _id=EntityId(file_model.id),
#             _filename=Filename(file_model.filename),
#             _uploaded_at=UploadedAt(file_model.uploaded_at),
#             _status=FileStatus(file_model.status),
#             _errors=file_model.errors and FileErrors(file_model.errors),
#             _user_id=file_model.user_id and UserId(file_model.user_id),
#             _deleted_at=file_model.deleted_at and DeletedAt(file_model.deleted_at),
#             _size=file_model.size and FileSize(file_model.size),
#             _file_data=None,
#         )
