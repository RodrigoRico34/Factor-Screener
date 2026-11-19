from sqlalchemy.orm import Session
import logging
from app.data.models.stock import create_stock, get_stock_by_ticker, update_stock, read_all_stocks

logger = logging.getLogger(__name__)

def import_stocks_core(db: Session, client):
    count = 0
    tickers = client().get_tickers()


    for ticker_data in tickers:
        try:
            existing = get_stock_by_ticker(db, ticker_data["Symbol"])
            if existing:
                update_stock(db, existing, ticker_data)
            else:
                create_stock(db, ticker_data)

            count += 1
        except Exception as e:
            logger.error(f"Failed to import {ticker_data['Symbol']}: {e}")

    db.commit()
    return {"imported": count}


def get_stocks_ranking(db: Session):
    return [
        {
            "ticker": s.ticker,
            "name": s.name,
            "sector": s.sector,
            "score_12m": None,
            "decile": None,
        }
        for s in read_all_stocks(db)
    ]