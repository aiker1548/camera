# from taskiq_aio_pika import AioPikaBroker
# from taskiq import TaskiqScheduler
# from taskiq.schedule_sources import LabelScheduleSource
# from dependency_injector.wiring import inject, Provide

# from application.camera.commands.save_camera_command import SaveCameraCommand
# from di.cameras import CamerasContainer
# from shared_kernel.building_blocks.application.mediator import Mediator
# from shared_kernel.loggers.main import get_presentation_logger
# from settings import Settings

# logger = get_presentation_logger()
# config = Settings()

# # Создание брокера AioPika на основе RabbitMQ
# broker = AioPikaBroker(f"{config.rabbitmq.url}")

# scheduler = TaskiqScheduler(
#     broker=broker,
#     sources=[LabelScheduleSource(broker)],
# )


# # Расписание "0 3 * * *" означает: запуск каждый день в 3:00 утра
# @broker.task(
#     schedule=[{"cron": "0 3 * * *", "args": []}],
#     queue="camera-scheduler_queue",
# )
# @inject
# async def get_camera_data_task(
#         mediator: Mediator = CamerasContainer.mediator(),
# ):
#     """
#     Задача для сбора данных с камеры.
#     Запускается по расписанию в 3 часа ночи каждый день.
#     """
#     logger.debug("Начало сбора данных с камеры")

#     command = SaveCameraCommand()
#     await mediator.send(command, context="camera")
#     logger.debug("Данные с камеры успешно собраны")
