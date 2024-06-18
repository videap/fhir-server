
from sqlalchemy.orm import Session
from typing import Generator
from contextlib import contextmanager
from fhir.utils.logger import logger
from fhir.environments.base import get_settings
from fhir.adapters.sql.handler import SessionLocal

# Start DB Session using dbconnector repo

S = get_settings()


def get_db() -> Session:
    session = SessionLocal()
    try:
        logger.debug("Starting DB session")
        #creates a session, run the operation, then yields it for the next run
        return session
    finally:
        logger.debug("Closing the DB session")
        session.close()

@contextmanager
def db_session() -> Generator[Session, None, None]:
    while True:
        yield get_db()
        break