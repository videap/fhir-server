from time import sleep
from fhir.adapters.events.handlers import fhirEventsListener
from fhir.adapters.events.interface import ListenerConfig
from fhir.utils.logger import logger
from fhir.environments.base import get_settings

def main():
    s = get_settings()
    rabbitmq_exchange = s.rabbitmq_exchange

    listeners = [
        {"exchange_name": rabbitmq_exchange, "queue_name": f"{rabbitmq_exchange}/queue_name_template", "routing_key": "routing_key_template", "on_message_callback": ..., "on_message_callback_error": ...},
    ]

    #Starting EventListener from MessageBroker in secondary threads
    #TODO Fix: sencondary threads is not working well with --reload app
    for listener in listeners:
        logger.info(f"Starting Listener to event {listener["routing_key"]}")
        Config = ListenerConfig(**listener)
        fhirEventsListener(Config).listen_to_events()

    while True:
        sleep(1) #Keep the main thread open as the listeners are running

if __name__ == '__main__':
    main()