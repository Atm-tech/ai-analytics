# models/outlet.py
from sqlalchemy import Column, Integer, String
from app.core.database import Base

class Outlet(Base):
    __tablename__ = "outlets"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    type = Column(String, default="outlet")  # "outlet" or "warehouse"
