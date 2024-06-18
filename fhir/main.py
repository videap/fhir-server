import logging
from fhir.environments.base import get_settings
from fhir.adapters.fast_api.routes import app
from fhir.utils.logger import logger


s = get_settings()

# Starting FastAPI WebServer
uvicorn_logger = logging.getLogger("uvicorn")
uvicorn_logger.handlers = logger.handlers

logger.info(f"Initializing fastAPI server: production: {s.production}, proxied: {s.proxied}.")
server = app