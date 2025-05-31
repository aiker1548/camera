# import functools
# import json
# import traceback

# import dramatiq
# from dependency_injector.wiring import inject
# from dramatiq import middleware
# from dramatiq.brokers.rabbitmq import RabbitmqBroker

# from application.video.commands.ML import start_video_processing
# from application.video.commands.ML.start_video_processing import StartVideoProcessingCommand
# from application.video.commands.validate_video_command import ValidateVideoCommand
# from di.videos import VideosContainer
# from infrastructure.integration_events.videos import \
#     VideoFileCreatedIntegrationEvent, StartVideoProcessingIntegrationEvent
# from settings import Settings
# from shared_kernel.building_blocks.application.mediator import Mediator
# from shared_kernel.loggers.main import get_presentation_logger

# # Logger
# logger = get_presentation_logger()


# def log_actor_exceptions(func):
#     @functools.wraps(func)
#     async def wrapper(*args, **kwargs):
#         try:
#             return await func(*args, **kwargs)
#         except Exception:
#             logger.critical(
#                 f"Exception in actor '{func.__name__}':\n{traceback.format_exc()}"
#             )
#             # raise

#     return wrapper


# # Broker
# rabbitmq_broker = RabbitmqBroker(
#     url=f"{Settings().rabbitmq.url}?heartbeat=0",
# )

# rabbitmq_broker.add_middleware(middleware.asyncio.AsyncIO())
# dramatiq.set_broker(rabbitmq_broker)


# # Heavy workers
# @dramatiq.actor(queue_name="cpu-bound_queue", time_limit=120 * 60 * 1_000)
# @inject
# @log_actor_exceptions
# async def validate_video(
#         event_data: dict,
#         mediator: Mediator = VideosContainer.mediator(),
# ):
#     command = ValidateVideoCommand(
#         event_data.get("file_id"),
#         event_data.get("camera_id"),
#         event_data.get("file_path"),
#     )
#     await mediator.send(command, context="video")


# @dramatiq.actor(queue_name="cpu-bound_queue", time_limit=120 * 60 * 1_000)
# @inject
# @log_actor_exceptions
# async def start_video_processing(
#         event_data: dict,
#         mediator: Mediator = VideosContainer.mediator(),
# ):
#     command = StartVideoProcessingCommand(
#         event_data.get("task_id"),
#         event_data.get("video_path"),
#         event_data.get("first_frame_path"),
#     )
#     await mediator.send(command, context="video")


# # Listnere handlers
# listeners: dict[str, tuple[dramatiq.Actor]] = {
#     VideoFileCreatedIntegrationEvent.__name__: (validate_video,),
#     StartVideoProcessingIntegrationEvent.__name__: (start_video_processing,),
# }


# @dramatiq.actor(queue_name="lite_queue")
# def handler_events(event_body):
#     logger.debug(f"handler_events received: {event_body}")
#     try:
#         event: dict = json.loads(event_body)
#         event_name = event.get("event_type")
#         if event_name not in listeners:
#             logger.error("Unexpected Event: " + event_name)
#             return

#         for listener in listeners[event_name]:
#             listener.send(event)
#     except json.JSONDecodeError as e:
#         logger.exception(f"Decoding JSON error: {e}")
#     except Exception:
#         logger.critical("Event error:\n" + traceback.format_exc())
