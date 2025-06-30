# app/utils/column_definitions.py

COLUMN_MAP = {
    # ✅ Base File (Products)
    "BARCODE": "barcode",
    "ARTICLE NAME": "article_name",
    "CATEGORY1": "category1",
    "CATEGORY2": "category2",
    "CATEGORY3": "category3",
    "CATEGORY4": "category4",
    "CATEGORY5": "category5",
    "CATEGORY6": "category6",
    "DIVISION": "division",
    "DEPARTMENT": "department",
    "SECTION": "section",
    "RSP": "rsp",
    "WSP": "wsp",
    "MRP": "mrp",
    "HSN CODE": "hsn_sac_code",
    "TAX %": "tax_name",  # e.g. GST 18%
    
    # ✅ Purchase File
    "SUPPLIER": "supplier",
    "GRC NO":"ENTRY_NO","ENTRY_NO": "grc_number",
    "NET AMT": "net_amount","PUR_QTY": "quantity",
    "PURCHASE PRICE": "purchase_price",  # WSP
    "PURCHASE DATE": "purchase_date",

    # ✅ Sales File
    "OUTLET": "outlet_name",
    "NET AMOUNT": "net_amount",
    "DATE": "date",

    # ✅ Closing Stock File
    "CLOSING QTY": "closing_quantity",
        "BARCODE": "barcode",
    "ARTICLE_NAME": "article_name",
    "ITEM_NAME": "article_name",  # if present, fallback
    "CATEGORY1": "category1",
    "CATEGORY2": "category2",
    "CATEGORY3": "category3",
    "CATEGORY4": "category4",
    "CATEGORY5": "category5",
    "CATEGORY6": "category6",
    "DIVISION": "division",
    "DEPARTMENT": "department",
    "SECTION": "section",
    "MRP": "mrp",
    "RSP": "rsp",
    "WSP": "wsp",
    "HSN_CODE": "hsn_sac_code",
    "TAX_NAME": "tax_name",

    # === Purchase-related ===
    "SUPPLIER NAME": "supplier",
    "SUPPLIER": "supplier",  # fallback
    "ENTRY_NO": "grc_number",
    "INVOICE NO": "grc_number",  # fallback alias
    "PURCHASE DATE": "purchase_date",
    "PUR_QTY": "quantity",
    "NET AMT": "net_amount",
    
    # === Sales-related ===
    "OUTLET": "outlet_name",
    "DATE": "date",

    # === Closing Stock-related ===
    "CLOSING QTY": "closing_quantity"
}
