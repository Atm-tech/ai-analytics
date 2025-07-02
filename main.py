# ISMS/main.py (to be added soon)

from fastapi import Depends
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from fastapi import FastAPI
from app.routers import upload_product, upload_purchase, upload_closing_stock, upload_sales
from app.routers import definition
import sys
import os
sys.path.append(os.path.dirname(__file__))
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
app = FastAPI()
app.include_router(upload_product.router, prefix="/api", tags=["Upload - Product Base"])
app.include_router(upload_purchase.router, prefix="/api", tags=["Upload - Purchase File"])
app.include_router(upload_closing_stock.router, prefix="/api", tags=["Upload - Closing Stock"])
app.include_router(upload_sales.router, prefix="/api", tags=["Upload - Sales File"])
app.include_router(definition.router)