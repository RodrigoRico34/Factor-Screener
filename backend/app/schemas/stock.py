from pydantic import BaseModel

class Stock(BaseModel):
    ticker: str
    name: str
    sector: str