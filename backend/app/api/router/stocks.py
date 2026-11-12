from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.stocks import import_stocks_core
from app.data.database import get_db
from app.data.tickers.sp500_github_client import SP500Github

router = APIRouter()

@router.post("/stocks/import")
def import_stocks(db: Session = Depends(get_db)):
    client = SP500Github
    try:
        return import_stocks_core(db, client)
    except SQLAlchemyError:
        db.rollback()
        #if there is an error with SQLAlchemy raise an exception code with status 503
        raise HTTPException(status_code=503, detail="Database unavailable")