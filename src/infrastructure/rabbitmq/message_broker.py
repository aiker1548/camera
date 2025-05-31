# import json
# from dataclasses import asdict

# from shared_kernel.building_blocks.infrastructure.integration_event import \
#     IntegrationEvent
# from shared_kernel.building_blocks.infrastructure.message_broker import \
#     MessageBroker


# class RabbitMQMessageBroker(MessageBroker):
#     """
#     TODO: Circulaar imports. (handler_events) 
#     """
#     def __init__(
#         self,
#         url: str,
#         exchange: str,
#         routing_key: str,
#         queue: str
#     ):
#         self.url = url
#         self.exchange = exchange
#         self.routing_key = routing_key
#         self.queue = queue

#     def publish(self, event: IntegrationEvent) -> None:
#         from presentation.worker.tasks.videos import handler_events  # noqa
#         event_dict = {
#             "event_id": str(event.event_id),
#             "event_timestamp": event.event_timestamp.isoformat(),
#             "event_type": event.event_type,
#             **asdict(event)
#         }

#         message = json.dumps(event_dict, default=str)

#         handler_events.send(message)
