from sqlalchemy.orm import Session
from sqlalchemy.dialects.mysql import insert
import logging

from app.data.models.stock import read_all_stocks
from app.data.models.price import Price

logger = logging.getLogger(__name__)


def import_prices_core(db: Session, client):
    stocks = read_all_stocks(db)
    tickers = [s.ticker for s in stocks]
    ticker_to_id = {s.ticker: s.id for s in stocks}

    prices = client().get_prices(tickers)

    rows = []
    for row in prices:
        stocks_id = ticker_to_id.get(row["ticker"])
        if stocks_id is None:
            continue
        rows.append({
            "stocks_id": stocks_id,
            "date": row["date"],
            "close": row["close"],
        })

    # Bulk insert, ignore duplicates (ON DUPLICATE KEY)
    batch_size = 5000
    count = 0
    for i in range(0, len(rows), batch_size):
        batch = rows[i:i + batch_size]
        stmt = insert(Price).values(batch)
        stmt = stmt.on_duplicate_key_update(close=stmt.inserted.close)
        db.execute(stmt)
        db.commit()
        count += len(batch)
        print(f"      {count}/{len(rows)} prices inserted...")

    return {"imported": len(rows), "skipped": 0}