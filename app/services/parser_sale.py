import pandas as pd
from sqlalchemy.orm import Session
from fastapi import UploadFile
from io import BytesIO
from datetime import datetime
from app.models.sale import Sale
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

async def process_sales_file(file: UploadFile, db: Session):
    content = await file.read()
    df = pd.read_excel(BytesIO(content))
    df = resolve_columns(df)

    required_cols = ["barcode", "quantity", "net_amount", "outlet_name", "date"]
    if not all(col in df.columns for col in required_cols):
        raise Exception("Missing required columns in uploaded sales file.")

    saved = 0

    for _, row in df.iterrows():
        barcode = str(row.get("barcode")).strip()
        qty = row.get("quantity")
        net_amt = row.get("net_amount")
        outlet_name = str(row.get("outlet_name")).strip()
        date_val = row.get("date")

        if not barcode or pd.isna(qty) or pd.isna(net_amt) or not outlet_name or pd.isna(date_val):
            continue

        try:
            if isinstance(date_val, str):
                date_val = pd.to_datetime(date_val).date()
            else:
                date_val = date_val.date()
        except Exception:
            continue

        outlet = get_or_create_outlet(outlet_name, db)

        exists = db.query(Sale).filter_by(barcode=barcode, outlet_id=outlet.id, date=date_val).first()
        if exists:
            continue

        sale = Sale(
            barcode=barcode,
            outlet_id=outlet.id,
            quantity=qty,
            net_amount=net_amt,
            date=date_val
        )
        db.add(sale)
        saved += 1

    db.commit()
    return {"sales_records_saved": saved}
