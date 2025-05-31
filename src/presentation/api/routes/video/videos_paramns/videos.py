# import uuid

# from fastapi import Query
# from pydantic import BaseModel
# from datetime import datetime
# from pydantic import Field

# from application.video.interfaces.persistence.reader import VideoFilters, VideoProgressedFilters
# from shared_kernel.building_blocks.domain.enums import TimeOfDay, TracingStatus, AnalysisType


# class FilterVideosParams(BaseModel):
#     video_name_or_id__subtext: str | None = Query(None,
#                                             description="Фильтр по названию видео")
#     camera_id__eq: int | None = Query(None)
#     user_id__in: list[uuid.UUID] = Field(Query(default_factory=list, description="Фильтр по User id"))
#     tracing__in: list[TracingStatus] | None = Field(Query(None))
#     time_of_day__in: list[TimeOfDay] | None = Field(Query(None))
#     duration__le: int | None = Query(None)
#     duration__ge: int | None = Query(None)
#     created_at__le: datetime | None = Query(None)
#     created_at__ge: datetime | None = Query(None)

#     def build_video_filters(self) -> VideoFilters:
#         return VideoFilters(
#             video_name_or_id__subtext=self.video_name_or_id__subtext,
#             camera_id__eq=self.camera_id__eq,
#             user_id__in=self.user_id__in,
#             tracing__in=self.tracing__in,
#             time_of_day__in=self.time_of_day__in,
#             duration__le=self.duration__le,
#             duration__ge=self.duration__ge,
#             created_at__le=self.created_at__le,
#             created_at__ge=self.created_at__ge,
#         )


# class FilterVideosProcessedParams(BaseModel):
#     video_name__subtext: str | None = Query(None,
#                                             description="Фильтр по названию видео")
#     owner_fullname_or_email__subtext: str | None = Query(None,
#                                                          description="Фильтр по ФИО или email пользователя")
#     video_id__eq: uuid.UUID | None = Query(None)
#     analysis_type__in: list[AnalysisType] | None = Field(Query(None))
#     time_of_day__in: list[TimeOfDay] | None = Field(Query(None))
#     duration__le: int | None = Query(None)
#     duration__ge: int | None = Query(None)
#     analysis_date__le: datetime | None = Query(None)
#     analysis_date__ge: datetime | None = Query(None)

#     def build_video_filters(self) -> VideoProgressedFilters:
#         return VideoProgressedFilters(
#             video_name__subtext=self.video_name__subtext,
#             owner_fullname_or_email__subtext=self.owner_fullname_or_email__subtext,
#             video_id__eq=self.video_id__eq,
#             analysis_type__in=self.analysis_type__in,
#             time_of_day__in=self.time_of_day__in,
#             duration__le=self.duration__le,
#             duration__ge=self.duration__ge,
#             analysis_date__le=self.analysis_date__le,
#             analysis_date__ge=self.analysis_date__ge,
#         )
