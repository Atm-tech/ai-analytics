# models/sale.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date
from app.core.database import Base

class Sale(Base):
    __tablename__ = "sales"
    id = Column(Integer, primary_key=True, index=True)
    barcode = Column(String, index=True)
    outlet_id = Column(Integer, ForeignKey("outlets.id"))
    quantity = Column(Float)
    net_amount = Column(Float)
    date = Column(Date)
