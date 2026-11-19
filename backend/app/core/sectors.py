from sqlalchemy.orm import Session
from app.data.models.stock import read_all_sectors


def get_sectors(db: Session) -> list[str]:
    return read_all_sectors(db)