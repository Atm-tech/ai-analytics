# models/closing_stock.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.core.database import Base

class ClosingStock(Base):
    __tablename__ = "closing_stock"
    id = Column(Integer, primary_key=True, index=True)
    barcode = Column(String, index=True)
    outlet_id = Column(Integer, ForeignKey("outlets.id"))
    closing_quantity = Column(Float)
