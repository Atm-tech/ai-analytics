# routers/analytics_router.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date
from app.core.database import get_db
from app.reports.speed_logic import classify_products_by_speed

router = APIRouter(prefix="/analyze", tags=["Analytics"])

@router.get("/speed-tiers")
def analyze_speed_tiers(db: Session = Depends(get_db)):
    today = date.today()
    return classify_products_by_speed(db, today)
