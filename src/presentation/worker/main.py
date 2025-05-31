# import importlib
# import logging

# import dramatiq
# from dramatiq import middleware
# from dramatiq.brokers.rabbitmq import RabbitmqBroker

# logger = logging.getLogger(__name__)

# rabbitmq_url = ("amqp://admin:"
#                 "admin@"
#                 "localhost:5672/")
# modules = [
#     "presentation.worker.tasks.camera",
# ]


# def bind_middlewares(broker: RabbitmqBroker) -> None:
#     broker.add_middleware(middleware.asyncio.AsyncIO())


# def build_dramatiq() -> None:
#     broker = RabbitmqBroker(url=rabbitmq_url)
#     bind_middlewares(broker)
#     dramatiq.set_broker(broker)
#     bind_tasks()


# def bind_tasks() -> None:
#     for module in modules:
#         importlib.import_module(module)


# build_dramatiq()
