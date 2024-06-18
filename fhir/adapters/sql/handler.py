from sqlalchemy import create_engine, Column, String, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./fhir.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Patient(Base):
    __tablename__ = "patients"
    id = Column(String, primary_key=True, index=True)
    resource = Column(JSON, nullable=False)

Base.metadata.create_all(bind=engine)
