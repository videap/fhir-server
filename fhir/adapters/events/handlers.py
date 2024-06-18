
import json
from typing import Dict, Any
from fhir.environments.base import get_settings
from fhir.adapters.events import interface as events_interface
from fhir.utils.logger import logger
from qconnector.components.rabbitmq_publisher import publish_message
from qconnector.components.rabbitmq_consumer import start_consumer_thread
from qconnector.utils.interface import ConnectionParams, PublisherSetup, ConsumerSetup, Message

class fhirEventsPublisher():

    def __init__(self, PS: events_interface.EventToPublish):
        self.S = get_settings()
        self.CP = ConnectionParams(host=self.S.rabbitmq_host, port=self.S.rabbitmq_port, user=self.S.rabbitmq_user.get_value(), password=self.S.rabbitmq_password.get_value())
        self.PS = PS

    def config(self, PS: events_interface.EventToPublish) -> None:
        """Use this function to override one of the values set in the __init__
        """

        self.queue_name = PS.queue_name
        self.routing_key = PS.routing_key
        self.exchange_name = PS.exchange_name
        self.exchange_type = PS.exchange_type
        self.publish_interval = PS.publish_interval
        self.on_confirmation_callback = PS.on_confirmation_callback

    def create_event(self, body:Dict[Any, Any], headers:Dict[Any, Any]) -> None:
        #TODO add event id here
        message = Message(body=json.dumps(body), headers=headers)
        publish_message(CP=self.CP, PS=PublisherSetup(**self.PS.model_dump()), message=message)


class fhirEventsListener:

    def __init__(self, CS: events_interface.ListenerConfig) -> None:
        self.S = get_settings()
        self.queue_name = CS.queue_name
        self.routing_key = CS.routing_key
        self.exchange_name = CS.exchange_name
        self.exchange_type = CS.exchange_type
        self.on_message_callback = CS.on_message_callback


        self.CP = ConnectionParams(host=self.S.rabbitmq_host, port=self.S.rabbitmq_port, user=self.S.rabbitmq_user.get_value(), password=self.S.rabbitmq_password.get_value())
        self.CS = ConsumerSetup(**CS.model_dump())

    def config(self, CS: events_interface.ListenerConfig) -> None:
        """Use this function to override one of the values set in the __init__
        """

        self.queue_name = CS.queue_name
        self.routing_key = CS.routing_key
        self.exchange_name = CS.exchange_name
        self.exchange_type = CS.exchange_type
        self.on_message_callback = CS.on_message_callback


    def listen_to_events(self) -> None:
        logger.info(f"Starting thread to consume messages from {self.exchange_name}/{self.queue_name}")
        start_consumer_thread(CP=self.CP, CS=self.CS)

