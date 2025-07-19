from datetime import date, datetime
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from app.models.product import Product
from app.models.purchase import Purchase
from app.models.sale import Sale
from app.models.stock import ClosingStock
from app.models.outlet import Outlet
from app.models.speed_tier_definition import SpeedTierDefinition

def classify_products_by_speed(db: Session, today: date):
    tiers = db.query(SpeedTierDefinition).order_by(SpeedTierDefinition.percentage.desc()).all()
    products = db.query(Product).all()
    results = []

    for product in products:
        barcode = product.barcode

        total_received = db.query(func.sum(Purchase.quantity))\
            .filter(Purchase.barcode == barcode).scalar() or 0

        total_sold = db.query(func.sum(Sale.quantity))\
            .filter(Sale.barcode == barcode).scalar() or 0

        first_purchase = db.query(func.min(Purchase.purchase_date))\
            .filter(Purchase.barcode == barcode).scalar()

        if not first_purchase or total_received == 0:
            continue

        days_so_far = max((today - first_purchase.date()).days, 1)
        sold_pct = total_sold / total_received * 100

        classification = None
        projected_class = None

        for tier in tiers:
            if sold_pct >= tier.percentage and days_so_far <= tier.days:
                classification = tier.name
                break
            projected_pct = (total_sold / days_so_far) * tier.days / total_received * 100
            if projected_pct >= tier.percentage and not projected_class:
                projected_class = f"potential {tier.name}"

        outlet_qty = db.query(func.sum(ClosingStock.closing_quantity))\
            .join(Outlet, ClosingStock.outlet_id == Outlet.id)\
            .filter(
                ClosingStock.barcode == barcode,
                Outlet.type == "outlet"
            ).scalar() or 0

        warehouse_qty = db.query(func.sum(ClosingStock.closing_quantity))\
            .join(Outlet, ClosingStock.outlet_id == Outlet.id)\
            .filter(
                ClosingStock.barcode == barcode,
                Outlet.type == "warehouse"
            ).scalar() or 0

        transfer_suggestion = None
        if outlet_qty == 0 and warehouse_qty > 0 and classification in ["superfast", "fast"]:
            transfer_suggestion = "Move stock to outlet urgently"

        results.append({
            "barcode": barcode,
            "name": product.article_name,
            "sold_pct": round(sold_pct, 2),
            "days_since_arrival": days_so_far,
            "classification": classification or "unclassified",
            "potential": projected_class,
            "transfer_suggestion": transfer_suggestion
        })

    return results
