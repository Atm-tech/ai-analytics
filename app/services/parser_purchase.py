import pandas as pd
from io import BytesIO
from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session
from app.models.purchase import Purchase
from app.models.product import Product
from app.utils.column_definitions import COLUMN_MAP

REQUIRED_PURCHASE_COLS = {"barcode", "grc_number", "net_amount", "quantity"}
REQUIRED_PRODUCT_COLS = {
    "barcode", "article_name",
    "category1", "category2", "category6",
    "division", "department",
    "mrp", "rsp",  # wsp is optional
    "hsn_sac_code", "tax_name"
}

def extract_tax_percent(tax_name: str) -> float:
    import re
    match = re.search(r"(\d{1,2})%", str(tax_name))
    return float(match.group(1)) if match else 0

def process_purchase_file(file: UploadFile, db: Session):
    try:
        contents = file.file.read()
        df = pd.read_excel(BytesIO(contents))

        # Standardize headers
        df.rename(columns=lambda col: COLUMN_MAP.get(col.strip().upper(), col.strip()), inplace=True)

        # Validate required columns for purchase logic
        missing = REQUIRED_PURCHASE_COLS - set(df.columns)
        if missing:
            raise HTTPException(status_code=400, detail=f"Missing purchase columns: {missing}")

        inserted, skipped = 0, 0
        for _, row in df.iterrows():
            barcode = str(row.get("barcode")).strip()
            grc_number = str(row.get("grc_number")).strip()

            # Skip duplicates
            if db.query(Purchase).filter_by(barcode=barcode, grc_number=grc_number).first():
                skipped += 1
                continue

            # Check product
            product = db.query(Product).filter_by(barcode=barcode).first()

            # If product doesn't exist, try to create
            if not product:
                # Validate required product fields
                missing_product_fields = [f for f in REQUIRED_PRODUCT_COLS if f not in df.columns]
                if missing_product_fields:
                    raise HTTPException(
                        status_code=400,
                        detail=f"New product missing column(s): {missing_product_fields}"
                    )

                product = Product(
                    barcode=barcode,
                    article_name=row.get("article_name"),
                    category1=row.get("category1"),
                    category2=row.get("category2"),
                    category3=row.get("category3"),
                    category4=row.get("category4"),
                    category5=row.get("category5"),
                    category6=row.get("category6"),
                    division=row.get("division"),
                    department=row.get("department"),
                    section=row.get("section"),
                    rsp=row.get("rsp"),
                    wsp=row.get("wsp"),
                    mrp=row.get("mrp"),
                    hsn_sac_code=row.get("hsn_sac_code"),
                    tax_name=row.get("tax_name"),
                    tax_percent=extract_tax_percent(row.get("tax_name"))
                )
                db.add(product)
                db.flush()

            # Insert purchase
            qty = float(row.get("quantity") or 0)
            net = float(row.get("net_amount") or 0)
            unit_price = round(net / qty, 2) if qty else 0

            purchase = Purchase(
                barcode=barcode,
                grc_number=grc_number,
                supplier=row.get("supplier"),
                quantity=qty,
                net_amount=net,
                unit_price=unit_price,
                rsp=row.get("rsp"),
                purchase_date=pd.to_datetime(row.get("purchase_date", pd.Timestamp.now()))
            )

            db.add(purchase)
            inserted += 1

        db.commit()
        return {"inserted": inserted, "skipped": skipped}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
