from fastapi import APIRouter, File, UploadFile, Form, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.core.database import get_db

# 🧠 Import all your parser functions
from app.services.parser_product import process_base_file
from app.services.parser_purchase import process_purchase_file
from app.services.parser_sale import process_sales_file
from app.services.parser_closing_stock import process_closing_stock_file

router = APIRouter(prefix="/api/upload", tags=["Upload"])

@router.post("")
async def upload_file(
    file: UploadFile = File(...),
    type: str = Form(...),
    db: Session = Depends(get_db)
):
    try:
        if type == "base":
            result = process_base_file(file, db)
        elif type == "purchase":
            result = process_purchase_file(file, db)
        elif type == "sale":
            result = await process_sales_file(file, db)
        elif type == "stock":
            result = await process_closing_stock_file(file, db)
        else:
            raise HTTPException(status_code=400, detail="Invalid file type")

        return JSONResponse(content={
            "message": f"{file.filename} uploaded and processed as {type}.",
            "result": result
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")
