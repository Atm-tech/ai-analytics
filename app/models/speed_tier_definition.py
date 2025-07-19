from sqlalchemy import Column, Integer, String, Float, Boolean
from app.core.database import Base

class SpeedTierDefinition(Base):
    __tablename__ = "speed_tier_definitions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)  # e.g. "superfast", "slow"
    percentage = Column(Float, nullable=False)  # e.g. 80
    days = Column(Integer, nullable=False)  # e.g. 90
    is_global = Column(Boolean, default=False)
    created_by = Column(String, nullable=True)  # Optional for user ownership
