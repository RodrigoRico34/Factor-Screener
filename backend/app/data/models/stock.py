from sqlalchemy import Column, String
from app.data.database import Base
from sqlalchemy.orm import Session


class Stock(Base):
    __tablename__ = "stocks"

    ticker = Column(String(50), primary_key=True)
    name = Column(String(100), nullable=False)
    sector = Column(String(50), nullable=False)


def read_all_stocks(db: Session) -> list[Stock]:
    return db.query(Stock).all()


def get_stock_by_ticker(db: Session, ticker: str):
    return db.query(Stock).filter_by(ticker=ticker).first()


def create_stock(db: Session, stock: dict):
    new_stock = Stock(
        ticker=stock["Symbol"],
        name=stock["Name"],
        sector=stock["Sector"]
    )
    db.add(new_stock)


def update_stock(db, existing, stock: dict):
    existing.name = stock["Name"]
    existing.sector = stock["Sector"]