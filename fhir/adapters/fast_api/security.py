from fastapi import HTTPException, Request, Depends
from starlette.middleware.base import BaseHTTPMiddleware
from fhir.environments.base import get_settings
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fhir.utils.logger import logger
import secrets

s = get_settings()

route = f"/{s.app_name}" if s.proxied else ""
noauth_routes = [f"{route}/thedocs", f"{route}/openapi.json", f"{route}/health", f"{route}/health", "/health"]

class VerifyAPIKeyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        api_key = request.headers.get('x-api-key')
        if request.url.path not in noauth_routes and api_key != s.api_key.get_value():
            msg = f"Request to {request.url} failed. API Key does not match."
            logger.error(msg)
            raise HTTPException(status_code=403, detail="Invalid API Key")
        response = await call_next(request)
        return response