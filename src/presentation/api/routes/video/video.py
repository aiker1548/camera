# from fastapi import APIRouter, Depends, File, UploadFile
# from uuid import UUID

# from dependency_injector.wiring import Provide, inject

# from application.auth.dto import JWTUserPayload
# from application.video import dto
# from application.video.commands.create_video_command import UploadVideoCommand
# from application.video.dto.get_video import VideosLimitsDTO
# from application.video.queries.get_video_by_id import GetVideoById
# from application.video.queries.get_video_processed import GetVideosProcessedQuery
# from application.video.queries.get_videos import GetVideosQuery
# from application.video.queries.get_videos_filters import GetVideosFiltersQuery

# from di.videos import VideosContainer
# from presentation.api.responses.base import OkResponse
# from presentation.api.routes.auth.dependencies.auth_dep import get_current_user
# from shared_kernel.building_blocks.application.dto import DTO
# from shared_kernel.building_blocks.application.mediator import Mediator
# from shared_kernel.building_blocks.application.pagination.dto import VideoOrderBy, VideoProcessedOrderBy
# from shared_kernel.building_blocks.presentaion.pagination_params import FilterPaginationParams
# from . import videos_paramns

# # router = APIRouter(tags=["Video"], dependencies=[Depends(get_current_user)])
# router = APIRouter(tags=["Video"])

# # http...../videos
# @router.get(
#     "/videos",
#     response_model=OkResponse[dto.VideosDTO],
# )
# @inject
# async def get_videos(
#         filter_params: videos_paramns.FilterVideosParams = Depends(videos_paramns.FilterVideosParams),
#         pagination_params: FilterPaginationParams[VideoOrderBy, VideoOrderBy.CREATED_AT] = Depends(
#             FilterPaginationParams[VideoOrderBy, VideoOrderBy.CREATED_AT]),
#         mediator: Mediator = Depends(Provide[VideosContainer.mediator]),
# ) -> OkResponse[dto.VideosDTO]:
#     """Return all video with optional filtering and pagination."""

#     filters = filter_params.build_video_filters()
#     pagination = pagination_params.build_pagination()

#     query = GetVideosQuery(
#         filters=filters,
#         pagination=pagination,
#     )

#     result: dto.VideosDTO = await mediator.send(query, "video")

#     return OkResponse[dto.VideosDTO](result=result)


# @router.get(
#     "/videos_filters",
#     response_model=OkResponse[VideosLimitsDTO],
# )
# @inject
# async def get_filters_inizialization_videos(
#         mediator: Mediator = Depends(Provide[VideosContainer.mediator]),
# ) -> OkResponse[VideosLimitsDTO]:
#     """Return all video with optional filtering and pagination."""

#     query = GetVideosFiltersQuery()

#     result: VideosLimitsDTO = await mediator.send(query, "video")

#     return OkResponse[VideosLimitsDTO](result=result)


# @router.post("/videos", response_model=dto.FileUploadResultDTO)
# @inject
# async def upload_video(
#         camera_id: int,
#         file: UploadFile = File(...),
#         mediator: Mediator = Depends(Provide[VideosContainer.mediator]),
#         current_user: JWTUserPayload = Depends(get_current_user),
# ):
#     """
#     Загружаем файл без дополнительной информации.
#     TODO: Узнать, что на пайплайн загрузки файла. В какой момент передается информация о видео.
#     """
#     file_content = await file.read()

#     command = UploadVideoCommand(
#         file_data=file_content,
#         filename=file.filename,
#         user_id=UUID(current_user.user_id),
#         camera_id=camera_id,
#     )
#     response: DTO = await mediator.send(command, context="video")
#     return response


# @router.get(
#     "/videos/{video_id}",
#     response_model=OkResponse[dto.DetailVideoDTO],
# )
# @inject
# async def get_video_by_id(
#         video_id: UUID,
#         mediator: Mediator = Depends(Provide[VideosContainer.mediator]),
# ) -> OkResponse[dto.DetailVideoDTO]:
#     """Return video, search by video_id"""

#     query = GetVideoById(video_id=video_id)

#     result = await mediator.send(query, "video")

#     return OkResponse[dto.DetailVideoDTO](result=result)


# @router.get(
#     "/videos/processed/",
#     response_model=OkResponse[dto.VideosProcessedDTO],
# )
# @inject
# async def get_videos_processed(
#         filter_params: videos_paramns.FilterVideosProcessedParams = Depends(videos_paramns.FilterVideosProcessedParams),
#         pagination_params: FilterPaginationParams[VideoProcessedOrderBy, VideoProcessedOrderBy.ANALYSIS_DATE] = Depends(
#             FilterPaginationParams[VideoProcessedOrderBy, VideoProcessedOrderBy.ANALYSIS_DATE]),
#         mediator: Mediator = Depends(Provide[VideosContainer.mediator]),
# ) -> OkResponse[dto.VideosDTO]:
#     """Return all video processed with optional filtering and pagination."""

#     filters = filter_params.build_video_filters()
#     pagination = pagination_params.build_pagination()

#     query = GetVideosProcessedQuery(
#         filters=filters,
#         pagination=pagination,
#     )

#     result: dto.VideosProcessedDTO = await mediator.send(query, "video")

#     return OkResponse[dto.VideosProcessedDTO](result=result)
