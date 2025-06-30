from sqlalchemy import Column, String, Float, DateTime
from datetime import datetime
from app.core.database import Base

class Product(Base):
    __tablename__ = "products"

    barcode = Column(String, primary_key=True, index=True)
    article_name = Column(String, nullable=False)

    category1 = Column(String, nullable=False)
    category2 = Column(String, nullable=False)
    category3 = Column(String, nullable=True)
    category4 = Column(String, nullable=True)  # may be used for pack size later
    category5 = Column(String, nullable=True)
    category6 = Column(String, nullable=False)

    division = Column(String, nullable=False)
    department = Column(String, nullable=False)
    section = Column(String, nullable=True)

    rsp = Column(Float, nullable=False)
    mrp = Column(Float, nullable=False)
    wsp = Column(Float, nullable=True)

    hsn_sac_code = Column(String, nullable=False)
    tax_name = Column(String, nullable=False)
    tax_percent = Column(Float, nullable=True)   # derived from tax_name

    pack_size = Column(String, nullable=True)     # optional, future use
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
