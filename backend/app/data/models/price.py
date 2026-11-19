from sqlalchemy import Column, Integer, Numeric, Date, ForeignKey, UniqueConstraint
from app.data.database import Base
from sqlalchemy.orm import Session


class Price(Base):
    __tablename__ = "prices"

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=False)
    close = Column(Numeric(12, 4), nullable=False)
    stocks_id = Column(Integer, ForeignKey("stocks.id"), nullable=False)

    __table_args__ = (
        UniqueConstraint("stocks_id", "date", name="uq_prices_stock_date"),
    )


def get_price(db: Session, stocks_id: int, date) -> Price | None:
    """Check if a price already exists for a given stock on a given date."""
    return db.query(Price).filter_by(stocks_id=stocks_id, date=date).first()


def create_price(db: Session, stocks_id: int, date, close: float):
    """Add a single price row to the session (not yet committed)."""
    new_price = Price(
        stocks_id=stocks_id,
        date=date,
        close=close,
    )
    db.add(new_price)