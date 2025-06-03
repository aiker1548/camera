import pika
from pika import ConnectionParameters, PlainCredentials

from src.shared_kernel.config import config

rabbit_connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host=config.RABBIT_HOST,
        port=config.RABBIT_PORT,
        credentials=pika.PlainCredentials(config.RABBIT_USER, config.RABBIT_PASS)
    )
)

rabbit_channel = rabbit_connection.channel()
rabbit_channel.queue_declare(queue=config.RABBIT_QUEUE_VIDEO_TASKS, durable=True)

RABBIT_PARAMS = ConnectionParameters(
    host=config.RABBIT_HOST,
    port=config.RABBIT_PORT,
    credentials=PlainCredentials(config.RABBIT_USER, config.RABBIT_PASS),
    heartbeat=600,
    blocked_connection_timeout=300
)

def get_rabbit_channel():
    """
    Returns the RabbitMQ channel for publishing messages.
    """
    
    rabbit_channel = rabbit_connection.channel()
    rabbit_channel.queue_declare(queue=config.RABBIT_QUEUE_VIDEO_TASKS, durable=True)

    return rabbit_channel