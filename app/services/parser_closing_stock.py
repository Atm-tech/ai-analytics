import pandas as pd
from sqlalchemy.orm import Session
from fastapi import UploadFile
from io import BytesIO
from app.models.stock import ClosingStock
from app.models.outlet import Outlet

# Helper to get or create an outlet
def get_or_create_outlet(name: str, db: Session, outlet_type: str = "outlet") -> Outlet:
    name = name.strip().title()
    outlet = db.query(Outlet).filter_by(name=name).first()
    if not outlet:
        outlet = Outlet(name=name, type=outlet_type)
        db.add(outlet)
        db.commit()
        db.refresh(outlet)
    return outlet

# Main parser
async def process_closing_stock_file(file: UploadFile, db: Session):
    content = await file.read()
    df = pd.read_excel(BytesIO(content))

    # Validate required columns
    if "MARKET" not in df.columns or "BARCODE" not in df.columns or "CLOSING" not in df.columns:
        raise Exception("Missing required columns: 'MARKET', 'BARCODE', 'CLOSING'")

    saved = 0

    # Clear previous stock data
    db.query(ClosingStock).delete()
    db.commit()

    for _, row in df.iterrows():
        outlet_name = str(row["MARKET"]).strip()
        barcode = str(row["BARCODE"]).strip()
        closing_qty = row["CLOSING"]

        if not outlet_name or not barcode or pd.isna(closing_qty):
            continue

        # Create or fetch outlet
        outlet = get_or_create_outlet(outlet_name, db)

        closing_stock = ClosingStock(
            outlet_id=outlet.id,
            barcode=barcode,
            closing_quantity=closing_qty
        )
        db.add(closing_stock)
        saved += 1

    db.commit()
    return {"closing_records_saved": saved}
