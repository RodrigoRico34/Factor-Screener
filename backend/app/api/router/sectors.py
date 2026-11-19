import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.sectors import get_sectors
from app.data.database import get_db

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/sectors", response_model=list[str])
def list_sectors(db: Session = Depends(get_db)):
    try:
        return get_sectors(db)
    except SQLAlchemyError:
        logger.exception("Database error on GET /sectors")
        # if there is an error with SQLAlchemy database, raise an exception 503
        raise HTTPException(status_code=503, detail="Database unavailable")