from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.prices import import_prices_core
from app.data.database import get_db
from app.data.prices.yfinance_client import YFinanceClient


router = APIRouter()


@router.post("/prices/import")
def import_prices(db: Session = Depends(get_db)):
    client = YFinanceClient
    try:
        return import_prices_core(db, client)
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=503, detail="Database unavailable")