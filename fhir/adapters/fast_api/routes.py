from httpconnector import server
from fastapi import Body, HTTPException, Depends
from typing import Annotated, List, Dict, Any, Literal
from fhir.environments.base import get_settings
from fhir.adapters.fast_api.security import VerifyAPIKeyMiddleware
from fhir.utils.logger import logger
from time import sleep
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.security import HTTPBasicCredentials
from pydantic import ValidationError

# Start Web Server
s = get_settings()
if s.proxied:
    route = f"/{s.app_name}"
else:
    route = ""

app = server.start(root_path = route, docs_url=None, redoc_url=None)

if s.production:
    app.add_middleware(VerifyAPIKeyMiddleware)

@app.get("/health") # type: ignore
def health() -> bool:
    return True

# User Routes