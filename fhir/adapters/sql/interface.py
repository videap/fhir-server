from pydantic import BaseModel
from typing import Dict,Any
from fhir.adapters.sql.handler import Patient
from fhir.adapters.sql.db_session import db_session
from sqlalchemy.orm import Session

class PatientDAO(BaseModel):
    id:str
    resource:Dict[str,Any]|None = None


    def _start_session(self):
        with db_session() as session:
            self._db:Session = session

    def create(self):
        self._start_session()

        db_patient = Patient(id=self.id, resource=self.resource)
        self._db.add(db_patient)
        self._db.commit()
        self._db.refresh(db_patient)
        return self

    def get(self):
        self._start_session()

        db_patient = self._db.query(Patient).filter(Patient.id == self.id).first()
        if db_patient is None:
            raise ValueError("Patient not found")
        return PatientDAO(id=self.id, resource=db_patient.to_dict()["resource"])


