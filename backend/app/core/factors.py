from sqlalchemy.orm import Session
import pandas as pd
import logging

from app.data.models.price import read_all_prices
from app.data.models.factor import (
    Factor,
    get_factor,
    create_factor,
    update_factor_momentum,
    read_factors_by_date,
    update_factor_decile,
    get_latest_factor_date,
)

logger = logging.getLogger(__name__)


def compute_momentum_core(db: Session):
    all_prices = read_all_prices(db)

    if not all_prices:
        return {"computed": 0}

    df = pd.DataFrame(all_prices, columns=["stocks_id", "date", "close"])
    df["close"] = df["close"].astype(float)

    pivot = df.pivot(index="date", columns="stocks_id", values="close").sort_index()
    pivot.index = pd.to_datetime(pivot.index)

    # Resample to monthly (last trading day of each month)
    monthly = pivot.resample("ME").last()

    # Momentum 12m = (price_now / price_12m_ago) - 1
    momentum_12m = (monthly / monthly.shift(12)) - 1

    # Drop rows where we don't have 12 months of history
    momentum_12m = momentum_12m.dropna(how="all")

    count = 0
    last_date = momentum_12m.index[-1].date()

    for stocks_id in momentum_12m.columns:
        # Get this stock's momentum value at the most recent month
        value = momentum_12m.loc[momentum_12m.index[-1], stocks_id]

        # Skip stocks with insufficient history (NaN momentum)
        if pd.isna(value):
            continue

        existing = get_factor(db, int(stocks_id), last_date)
        if existing:
            update_factor_momentum(existing, round(float(value), 6))
        else:
            create_factor(db, int(stocks_id), last_date, round(float(value), 6))

        count += 1

    db.commit()
    return {"computed": count}


def classify_deciles_core(db: Session):
    # Get the most recent date that has momentum values
    latest = get_latest_factor_date(db)

    if not latest:
        return {"classified": 0}

    factors = read_factors_by_date(db, latest)

    # Build a Series of momentum values indexed by factor ID
    data = {f.id: f.momentum_12m for f in factors if f.momentum_12m is not None}

    if not data:
        return {"classified": 0}

    series = pd.Series(data)

    # Classify into deciles (1 = worst, 10 = best)
    deciles = pd.qcut(series, 10, labels=range(1, 11), duplicates="drop")

    factor_by_id = {f.id: f for f in factors}

    count = 0
    for factor_id, decile in deciles.items():
        update_factor_decile(factor_by_id[factor_id], int(decile))
        count += 1

    db.commit()
    return {"classified": count}
