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

