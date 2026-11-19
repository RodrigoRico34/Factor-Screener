from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.factors import compute_momentum_core, classify_deciles_core
from app.data.database import get_db

router = APIRouter()


@router.post("/factors/compute")
def compute_factors(db: Session = Depends(get_db)):
    try:
        return compute_momentum_core(db)
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=503, detail="Database unavailable")


@router.post("/factors/deciles")
def classify_deciles(db: Session = Depends(get_db)):
    try:
        return classify_deciles_core(db)
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=503, detail="Database unavailable")