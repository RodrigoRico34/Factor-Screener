from sqlalchemy.orm import Session
import logging

from app.data.models.stock import read_all_stocks
from app.data.models.price import get_price, create_price

logger = logging.getLogger(__name__)


def import_prices_core(db: Session, client):
    stocks = read_all_stocks(db)
    tickers = [s.ticker for s in stocks]

    # Map each ticker to its database ID for O(1) lookup instead of querying the DB per row 
    ticker_to_id = {s.ticker: s.id for s in stocks}

    prices = client().get_prices(tickers)

    count = 0
    skipped = 0

    for row in prices:
        stocks_id = ticker_to_id.get(row["ticker"])

        if stocks_id is None:
            logger.warning(f"Ticker {row['ticker']} not found in stocks table, skipping")
            continue

        existing = get_price(db, stocks_id, row["date"])
        if existing:
            skipped += 1
            continue

        try:
            create_price(db, stocks_id, row["date"], row["close"])
            count += 1
        except Exception as e:
            logger.error(f"Failed to insert price for {row['ticker']} on {row['date']}: {e}")

    db.commit()
    return {"imported": count, "skipped": skipped}