# routers/speed_tier_router.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.speed_tier_definition import SpeedTierDefinition

router = APIRouter(prefix="/api/definitions", tags=["Speed Tiers"])

@router.get("/speed-tiers")
def get_speed_tiers(db: Session = Depends(get_db)):
    tiers = db.query(SpeedTierDefinition).all()
    return [{
        "id": t.id,
        "name": t.name,
        "percentage": t.percentage,
        "days": t.days,
        "is_global": t.is_global
    } for t in tiers]

from fastapi import HTTPException
from pydantic import BaseModel
from typing import List

class SpeedTierInput(BaseModel):
    name: str
    percentage: float
    days: int

class SpeedTierList(BaseModel):
    tiers: List[SpeedTierInput]

@router.post("/speed-tiers")
def save_speed_tiers(payload: SpeedTierList, db: Session = Depends(get_db)):
    # Delete non-global tiers before replacing
    db.query(SpeedTierDefinition).filter(SpeedTierDefinition.is_global == False).delete()
    db.commit()

    for t in payload.tiers:
        if not t.name or t.percentage < 0 or t.days <= 0:
            raise HTTPException(status_code=400, detail="Invalid tier values")
        db.add(SpeedTierDefinition(
            name=t.name,
            percentage=t.percentage,
            days=t.days,
            is_global=False
        ))

    db.commit()
    return {"message": "Speed tiers saved"}
