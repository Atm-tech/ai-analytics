from fastapi import APIRouter, UploadFile, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.parser_purchase import process_purchase_file

router = APIRouter()

@router.post("/upload/purchase")
async def upload_purchase_file(file: UploadFile, db: Session = Depends(get_db)):
    return await process_purchase_file(file, db)
