# import uuid
# from dataclasses import dataclass

# from shared_kernel.building_blocks.infrastructure.integration_event import \
#     IntegrationEvent


# @dataclass(frozen=True)
# class VideoFileCreatedIntegrationEvent(IntegrationEvent):
#     file_id: str
#     camera_id: int
#     file_path: str

# @dataclass(frozen=True)
# class StartVideoProcessingIntegrationEvent(IntegrationEvent):
#     task_id: uuid.UUID
#     video_path: str
#     first_frame_path: str