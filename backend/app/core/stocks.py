from sqlalchemy.orm import Session
import logging
from app.data.models.stock import create_stock, get_stock_by_ticker, update_stock, read_all_stocks
from app.data.models.factor import get_latest_factors_map

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


ALLOWED_SORT_FIELDS = ("ticker", "name", "sector", "score_12m", "decile")
ALLOWED_ORDERS = ("asc", "desc")


def sort_stocks(rows: list[dict], sort_by: str, order: str) -> list[dict]:
    if sort_by not in ALLOWED_SORT_FIELDS:
        raise ValueError(
            f"Invalid sort_by '{sort_by}'. Allowed values: {', '.join(ALLOWED_SORT_FIELDS)}"
        )
    if order not in ALLOWED_ORDERS:
        raise ValueError(
            f"Invalid order '{order}'. Allowed values: {', '.join(ALLOWED_ORDERS)}"
        )

    # rows without a value go last
    with_value = [row for row in rows if row[sort_by] is not None]
    without_value = [row for row in rows if row[sort_by] is None]

    def sort_key(row):
        value = row[sort_by]
        # lowercase text so "apple" and "Apple" are sorted together
        return value.lower() if isinstance(value, str) else value

    with_value.sort(key=sort_key, reverse=(order == "desc"))
    return with_value + without_value


def get_stocks_ranking(
    db: Session,
    sector: str | None = None,
    sort_by: str = "score_12m",
    order: str = "desc",
):
    factors_map = get_latest_factors_map(db)

    rows = []
    for s in read_all_stocks(db, sector):
        factor = factors_map.get(s.id)
        rows.append({
            "ticker": s.ticker,
            "name": s.name,
            "sector": s.sector,
            "score_12m": round(float(factor.momentum_12m), 6) if factor and factor.momentum_12m is not None else None,
            "decile": int(factor.decile) if factor and factor.decile is not None else None,
        })

    return sort_stocks(rows, sort_by, order)