import pandas as pd
from io import BytesIO
from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session
from app.models.product import Product
from app.utils.column_definitions import COLUMN_MAP

REQUIRED_PRODUCT_COLS = {
    "barcode", "article_name",
    "category1", "category2", "category6",
    "division", "department",
    "mrp", "rsp", "hsn_sac_code", "tax_name"
}

def extract_tax_percent(tax_name: str) -> float:
    import re
    match = re.search(r"(\d{1,2})%", str(tax_name))
    return float(match.group(1)) if match else 0

def process_base_file(file: UploadFile, db: Session):
    try:
        contents = file.file.read()
        df = pd.read_excel(BytesIO(contents))

        # Normalize column names
        df.rename(columns=lambda col: COLUMN_MAP.get(col.strip().upper(), col.strip()), inplace=True)

        # Check required product fields
        missing = REQUIRED_PRODUCT_COLS - set(df.columns)
        if missing:
            raise HTTPException(status_code=400, detail=f"Missing product columns: {missing}")

        inserted, updated = 0, 0

        for _, row in df.iterrows():
            barcode = str(row.get("barcode")).strip()

            product = db.query(Product).filter_by(barcode=barcode).first()

            values = {
                "article_name": row.get("article_name"),
                "category1": row.get("category1"),
                "category2": row.get("category2"),
                "category3": row.get("category3"),
                "category4": row.get("category4"),
                "category5": row.get("category5"),
                "category6": row.get("category6"),
                "division": row.get("division"),
                "department": row.get("department"),
                "section": row.get("section"),
                "rsp": row.get("rsp"),
                "mrp": row.get("mrp"),
                "wsp": row.get("wsp"),
                "hsn_sac_code": row.get("hsn_sac_code"),
                "tax_name": row.get("tax_name"),
                "tax_percent": extract_tax_percent(row.get("tax_name")),
            }

            if product:
                for k, v in values.items():
                    setattr(product, k, v)
                updated += 1
            else:
                new_product = Product(barcode=barcode, **values)
                db.add(new_product)
                inserted += 1

        db.commit()
        return {"inserted": inserted, "updated": updated}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
