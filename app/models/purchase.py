from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class Purchase(Base):
    __tablename__ = "purchases"

    id = Column(Integer, primary_key=True, index=True)
    barcode = Column(String, ForeignKey("products.barcode"), index=True, nullable=False)
    supplier = Column(String, nullable=True)
    grc_number = Column(String, index=True, nullable=False)
    quantity = Column(Float, nullable=True)
    
    net_amount = Column(Float, nullable=True)     # total amount paid for qty ✅
    unit_price = Column(Float, nullable=True)     # calculated: net / qty ✅

    rsp = Column(Float, nullable=True)
    purchase_date = Column(DateTime, default=datetime.utcnow)

    product = relationship("Product", backref="purchases")

    __table_args__ = (
        UniqueConstraint('barcode', 'grc_number', name='uq_barcode_grc'),
    )
