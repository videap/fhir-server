from httpconnector import server
from fastapi import Body, HTTPException, Depends
from typing import Annotated, List, Dict, Any, Literal
from fhir.environments.base import get_settings
from fhir.adapters.fast_api.security import VerifyAPIKeyMiddleware
from fhir.utils.logger import logger
from fhir.adapters.sql.interface import PatientDAO
from pydantic import ValidationError

# Start Web Server
s = get_settings()
if s.proxied:
    route = f"/{s.app_name}"
else:
    route = ""

app = server.start(root_path = route, redoc_url=None)

if s.production:
    app.add_middleware(VerifyAPIKeyMiddleware)

@app.get("/health") # type: ignore
def health() -> bool:
    return True

# Routes
@app.post("/fhir/Patient", response_model=PatientDAO)
def create_patient(patient: PatientDAO) -> PatientDAO:
    patient.create()
    return patient

@app.get("/fhir/Patient/{id}", response_model=PatientDAO)
def get_patient(id: str) -> PatientDAO:
    db_patient = PatientDAO(id=id)
    try:
        return db_patient.get()
    except ValueError:
        raise HTTPException(status_code=404, detail="Patient not found")
