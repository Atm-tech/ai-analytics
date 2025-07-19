import pandas as pd
from io import BytesIO
from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app.models.purchase import Purchase
from app.models.product import Product
from app.utils.column_resolver import resolve_columns

REQUIRED_PURCHASE_COLS = {"barcode", "grc_number", "net_amount", "gross_amount", "quantity", "supplier"}

REQUIRED_PRODUCT_COLS = {
    "barcode", "article_name", "category2", "category6",
    "division", "department", "mrp", "rsp", "hsn_sac_code"
}

def process_purchase_file(file: UploadFile, db: Session):
    try:
        contents = file.file.read()
        df = pd.read_excel(BytesIO(contents))
        df = resolve_columns(df)

        missing = REQUIRED_PURCHASE_COLS - set(df.columns)
        if missing:
            raise HTTPException(status_code=400, detail=f"Missing purchase columns: {missing}")

        inserted = 0
        updated_products = 0
        updated_purchases = 0
        skipped_rows = []

        for _, row in df.iterrows():
            try:
                barcode = str(row.get("barcode")).strip()
                grc_number = str(row.get("grc_number")).strip()
                supplier = row.get("supplier")

                if pd.isna(supplier) or not str(supplier).strip():
                    raise Exception("Supplier is missing")

                gross = float(row.get("gross_amount") or 0)
                net = float(row.get("net_amount") or 0)
                qty = float(row.get("quantity") or 0)
                unit_price = round(net / qty, 2) if qty else 0

                # Tax calc from net - gross
                gst_percent = round(((net - gross) / gross) * 100, 2) if gross else 0
                tax_name = f"GST {gst_percent}%" if gst_percent > 0 else "GST 0%"

                # 🔁 Update or insert product
                product = db.query(Product).filter_by(barcode=barcode).first()
                if product:
                    product.article_name = row.get("article_name")
                    product.category1 = row.get("category1") or "UNDEFINED"
                    product.category2 = row.get("category2")
                    product.category3 = row.get("category3")
                    product.category4 = row.get("category4")
                    product.category5 = row.get("category5")
                    product.category6 = row.get("category6")
                    product.division = row.get("division")
                    product.department = row.get("department")
                    product.section = row.get("section")
                    product.rsp = row.get("rsp")
                    product.wsp = row.get("wsp")
                    product.mrp = row.get("mrp")
                    product.hsn_sac_code = row.get("hsn_sac_code")
                    product.tax_name = tax_name
                    product.tax_percent = gst_percent
                    product.pack_size = row.get("pack_size")
                    product.last_updated = datetime.now()
                    updated_products += 1
                else:
                    product = Product(
                        barcode=barcode,
                        article_name=row.get("article_name"),
                        category1=row.get("category1") or "UNDEFINED",
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
                        tax_name=tax_name,
                        tax_percent=gst_percent,
                        pack_size=row.get("pack_size"),
                        last_updated=datetime.now()
                    )
                    db.add(product)
                    db.flush()

                # 🔁 Update or insert purchase
                purchase = db.query(Purchase).filter_by(barcode=barcode, grc_number=grc_number).first()
                if purchase:
                    purchase.quantity = qty
                    purchase.net_amount = net
                    purchase.unit_price = unit_price
                    purchase.rsp = row.get("rsp")
                    purchase.purchase_date = pd.to_datetime(row.get("purchase_date", datetime.now()))
                    purchase.supplier = supplier
                    updated_purchases += 1
                else:
                    purchase = Purchase(
                        barcode=barcode,
                        grc_number=grc_number,
                        supplier=supplier,
                        quantity=qty,
                        net_amount=net,
                        unit_price=unit_price,
                        rsp=row.get("rsp"),
                        purchase_date=pd.to_datetime(row.get("purchase_date", datetime.now()))
                    )
                    db.add(purchase)
                    inserted += 1

            except Exception as row_error:
                db.rollback()
                skipped_rows.append({
                    "barcode": str(row.get("barcode")),
                    "grc_number": str(row.get("grc_number")),
                    "reason": str(row_error)
                })

        db.commit()

        return {
            "inserted": inserted,
            "updated_purchases": updated_purchases,
            "updated_products": updated_products,
            "skipped": len(skipped_rows),
            "skipped_rows": skipped_rows
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")
