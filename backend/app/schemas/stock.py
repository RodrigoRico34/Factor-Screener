from pydantic import BaseModel


class Stock(BaseModel):
    ticker: str
    name: str
    sector: str


class StockRanking(Stock):
    score_12m: float | None = None
    decile: int | None = None