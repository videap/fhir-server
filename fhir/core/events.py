from fhir.adapters.events.interface import EventToPublish
from fhir.adapters.events.handlers import fhirEventsPublisher
from fhir.utils.logger import logger
from fhir.environments.base import get_settings
from contracts.base import Contract
from pika import BasicProperties

rabbitmq_exchange = get_settings().rabbitmq_exchange

def generate_event(event:Contract, exchange:str) -> None:

    event_name = type(event).__name__
    logger.info(f"Created event {event_name}")

    # Setting up the publisher
    PS = EventToPublish(queue_name=f"{exchange}/{event_name}",
                        routing_key=event_name,
                        exchange_name=exchange,
                        on_confirmation_callback_error=on_generate_event_error)

    EventCreator = fhirEventsPublisher(PS=PS)
    EventCreator.create_event(body=event.body.model_dump(), headers=event.headers.model_dump())

# On events
def on_event(body:bytes, properties:BasicProperties, event:str) -> None:
    logger.info(f"Event callback triggered.")

def on_callback_error(body:bytes, properties: BasicProperties) -> None:
    logger.error("Error processing event callback")

def on_generate_event_error(body:bytes, properties: BasicProperties) -> None:
    logger.error("Error when generating event")
