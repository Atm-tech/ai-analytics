import pandas as pd
from sqlalchemy.orm import Session
from fastapi import UploadFile
from io import BytesIO
from app.models.stock import ClosingStock
from app.models.outlet import Outlet
from app.utils.column_resolver import resolve_columns

def get_or_create_outlet(name: str, db: Session, outlet_type: str = "outlet") -> Outlet:
    name = name.strip().title()
    outlet = db.query(Outlet).filter_by(name=name).first()
    if not outlet:
        outlet = Outlet(name=name, type=outlet_type)
        db.add(outlet)
        db.commit()
        db.refresh(outlet)
    return outlet

def process_closing_stock_file(file: UploadFile, db: Session):
    from datetime import datetime
    content = file.file.read()
    df = pd.read_excel(BytesIO(content))
    df = resolve_columns(df)

    required = {"outlet_name", "barcode", "closing_quantity"}
    if not required.issubset(df.columns):
        raise ValueError(f"Missing required columns: {required - set(df.columns)}")

    saved = 0
    db.query(ClosingStock).delete()
    db.commit()

    for _, row in df.iterrows():
        outlet_name = str(row["outlet_name"]).strip()
        barcode = str(row["barcode"]).strip()
        closing_qty = row["closing_quantity"]

        if not outlet_name or not barcode or pd.isna(closing_qty):
            continue

        outlet = get_or_create_outlet(outlet_name, db)

        closing_stock = ClosingStock(
            outlet_id=outlet.id,
            barcode=barcode,
            closing_quantity=closing_qty
            
        )
        db.add(closing_stock)
        saved += 1

    db.commit()
    return {"saved": saved, "skipped": len(df) - saved, "total": len(df)}
