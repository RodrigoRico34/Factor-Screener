from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.stocks import import_stocks_core, get_stocks_ranking
from app.data.database import get_db
from app.data.tickers.sp500_github_client import SP500Github
from app.schemas.stock import StockRanking

router = APIRouter()


@router.get("/stocks", response_model=list[StockRanking])
def list_stocks(
    sector: str | None = Query(default=None, description="Filter by GICS sector (case-insensitive)"),
    sort_by: str = Query(default="score_12m", description="ticker, name, sector, score_12m or decile"),
    order: str = Query(default="desc", description="asc or desc"),
    db: Session = Depends(get_db),
):
    try:
        return get_stocks_ranking(db, sector, sort_by, order)
    except ValueError as exc:
        # invalid sort_by or order: tell the client what is wrong
        raise HTTPException(status_code=400, detail=str(exc))
    except SQLAlchemyError:
        # if there is an error with SQLAlchemy database, raise an exception 503
        raise HTTPException(status_code=503, detail="Database unavailable")


@router.post("/stocks/import")
def import_stocks(db: Session = Depends(get_db)):
    client = SP500Github
    try:
        return import_stocks_core(db, client)
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=503, detail="Database unavailable")