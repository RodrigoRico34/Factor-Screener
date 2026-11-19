from sqlalchemy import Column, Integer, String, func
from app.data.database import Base
from sqlalchemy.orm import Session


class Stock(Base):
    __tablename__ = "stocks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ticker = Column(String(10), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    sector = Column(String(45), nullable=False)


def read_all_stocks(db: Session, sector: str | None = None) -> list[Stock]:
    query = db.query(Stock)
    #if sector missing or empty, no filter
    if sector:
        # compare lowercase on both sides so the filter ignores case
        query = query.filter(func.lower(Stock.sector) == sector.strip().lower())
    return query.order_by(Stock.ticker).all()


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


def read_all_sectors(db: Session) -> list[str]:
    #order_by to filter by Alphabetical order, and distinct() removes duplicates
    rows = db.query(Stock.sector).distinct().order_by(Stock.sector).all()
    #.all() returns tuples like ("Energy",), so row[0] extracts the text
    return [row[0] for row in rows]