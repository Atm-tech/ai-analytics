# crud/speed_tier_crud.py

from sqlalchemy.orm import Session
from app.models.speed_tier_definition import SpeedTierDefinition

def seed_speed_tiers(db: Session):
    if db.query(SpeedTierDefinition).filter_by(is_global=True).first():
        return {"message": "Speed tiers already seeded."}

    tiers = [
        {"name": "superfast", "percentage": 80, "days": 90},
        {"name": "fast", "percentage": 60, "days": 90},
        {"name": "slow", "percentage": 30, "days": 90}
    ]

    for t in tiers:
        db.add(SpeedTierDefinition(
            name=t["name"],
            percentage=t["percentage"],
            days=t["days"],
            is_global=True
        ))

    db.commit()
    return {"message": "Speed tiers seeded."}
