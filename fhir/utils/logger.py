import logging
from nanologger import Logger
from fhir.environments.base import get_settings

# Settings
_settings = get_settings()


logger = Logger(level=_settings.log_level, production=_settings.production).log


# PROPAGATE logger to all libs
for name, sublogger in logging.Logger.manager.loggerDict.items():
    if isinstance(sublogger, logging.Logger):  # Filter out placeholders
        sublogger.setLevel(logging.WARNING)  # Set level
        sublogger.handlers = logger.handlers  # Set handlers
        sublogger.propagate = False