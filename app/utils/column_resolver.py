# app/utils/column_resolver.py

import pandas as pd
import difflib
import os
from collections import defaultdict
from app.utils.column_definitions import column_aliases

CONFIG_PATH = "configuration.xlsx"
FALLBACK_MAP = {}

# Columns to skip completely
SKIP_COLUMNS = {"ITEM NAME", "ITEM_NAME", "item name", "item_name"}

# Step 1: Build reverse alias lookup map
def build_reverse_map():
    reverse = {}
    for key, aliases in column_aliases.items():
        for alias in aliases:
            cleaned = alias.strip().upper()
            reverse[cleaned] = key
    return reverse

REVERSE_MAP = build_reverse_map()

# Step 2: Fallback from config descriptions
def build_fallback_map():
    global FALLBACK_MAP
    if not os.path.exists(CONFIG_PATH):
        return

    try:
        df = pd.read_excel(CONFIG_PATH, header=None)
        for i in range(len(df.columns)):
            raw_header = str(df.iloc[0, i]).strip().upper()
            description = str(df.iloc[1, i]).strip().lower()

            target = REVERSE_MAP.get(raw_header)
            if not target:
                continue

            for word in description.split():
                if word and word not in FALLBACK_MAP:
                    FALLBACK_MAP[word] = target
    except Exception as e:
        print(f"[column_resolver] ⚠️ Failed to load config: {e}")

build_fallback_map()

# Step 3: Resolve a single column
def resolve_column(header: str) -> str:
    header_clean = header.strip().upper()

    # 1. Exact match
    if header_clean in REVERSE_MAP:
        return REVERSE_MAP[header_clean]

    # 2. Fallback description keywords
    for word in header.lower().split():
        if word in FALLBACK_MAP:
            return FALLBACK_MAP[word]

    # 3. Fuzzy match
    close = difflib.get_close_matches(header_clean, REVERSE_MAP.keys(), n=1, cutoff=0.85)
    if close:
        return REVERSE_MAP[close[0]]

    # 4. Unresolved
    return f"UNRESOLVED:{header_clean}"

# Step 4: Detect duplicates in resolved names
def detect_duplicates(headers: list[str]):
    mapping = defaultdict(list)

    for original in headers:
        resolved = resolve_column(original)
        mapping[resolved].append(original)

    duplicates = {k: v for k, v in mapping.items() if len(v) > 1}

    if duplicates:
        print("\n🚨 Duplicate header resolutions detected:")
        for resolved_name, originals in duplicates.items():
            print(f" - '{resolved_name}' ← {originals}")
        raise ValueError(f"Duplicate resolved columns: {list(duplicates.keys())}")

    return mapping

# Step 5: Apply resolution to DataFrame
def resolve_columns(df: pd.DataFrame) -> pd.DataFrame:
    raw_headers = list(df.columns)
    print("💡 Raw headers from file:", raw_headers)

    # Remove skipped columns
    cleaned_headers = [h for h in raw_headers if h.strip() not in SKIP_COLUMNS]
    if len(cleaned_headers) < len(raw_headers):
        skipped = [h for h in raw_headers if h.strip() in SKIP_COLUMNS]
        print(f"🟡 Skipped headers: {skipped}")
        df = df[cleaned_headers]

    resolved = []
    for h in df.columns:
        col = resolve_column(h)
        print(f"🧩 Resolving '{h}' → '{col}'")
        resolved.append(col)

    detect_duplicates(list(df.columns))
    df.columns = resolved
    print("✅ Final resolved headers:", resolved)
    return df
