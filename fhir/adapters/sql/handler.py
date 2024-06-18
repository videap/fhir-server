from __future__ import annotations
from typing import Dict, Any
from sqlalchemy import create_engine, Column, String, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./fhir.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def class_to_dict(cls: Patient) -> Dict[Any, Any]:
    # Converts the object's attributes to a dictionary
    return {class_attr.name: getattr(cls, class_attr.name) for class_attr in cls.__table__.columns}

class Patient(Base):
    __tablename__ = "patients"
    id = Column(String, primary_key=True, index=True)
    resource = Column(JSON, nullable=False)

    def to_dict(self) -> Dict[Any, Any]:
        return class_to_dict(self)

Base.metadata.create_all(bind=engine)
