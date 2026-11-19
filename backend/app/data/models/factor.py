from sqlalchemy import Column, Integer, Double, Date, ForeignKey, UniqueConstraint, CheckConstraint
from app.data.database import Base
from sqlalchemy.orm import Session


class Factor(Base):
    __tablename__ = "factors"

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=False)
    momentum_1m = Column(Double, nullable=True)
    momentum_3m = Column(Double, nullable=True)
    momentum_6m = Column(Double, nullable=True)
    momentum_12m = Column(Double, nullable=True)
    decile = Column(Integer, nullable=True)
    stocks_id = Column(Integer, ForeignKey("stocks.id"), nullable=False)

    __table_args__ = (
        UniqueConstraint("stocks_id", "date", name="uq_factors_stock_date"),
        CheckConstraint("decile BETWEEN 1 AND 10", name="chk_decile"),
    )


def get_factor(db: Session, stocks_id: int, date) -> Factor | None:
    return db.query(Factor).filter_by(stocks_id=stocks_id, date=date).first()


def create_factor(db: Session, stocks_id: int, date, momentum_12m: float):
    new_factor = Factor(
        stocks_id=stocks_id,
        date=date,
        momentum_12m=momentum_12m,
    )
    db.add(new_factor)


def update_factor_momentum(existing: Factor, momentum_12m: float):
    existing.momentum_12m = momentum_12m