import hashlib
import os
from datetime import datetime

import pandas as pd

COLUMNS = [
    "record_id", "source", "source_id", "sender", "customer_name", "product",
    "quantity", "unit_price", "total_amount", "city", "order_date",
    "received_at", "ingested_at",
]

RENAME = {
    "order_id": "source_id", "order_no": "source_id",
    "customer": "customer_name", "client": "customer_name",
    "item": "product", "product_name": "product",
    "qty": "quantity", "amount": "quantity",
    "price": "unit_price", "unit price": "unit_price",
    "location": "city",
    "date": "order_date", "created_at": "order_date",
    "updated_at": "received_at",
}


def make_id(source, source_id):
    return hashlib.md5(f"{source}|{source_id}".encode()).hexdigest()


def standardize(df, source):
    if df.empty:
        return pd.DataFrame(columns=COLUMNS)

    df = df.copy()

    df.columns = [str(c).strip().lower() for c in df.columns]
    df = df.rename(columns=RENAME)
    for col in COLUMNS:
        if col not in df.columns:
            df[col] = None

    now = datetime.now()
    df["source"] = source

    for col in ["customer_name", "product", "city", "sender"]:
        df[col] = df[col].astype("string").str.strip()
    df["product"] = df["product"].str.title()
    df["city"] = df["city"].str.title().fillna("Unknown")
    df["customer_name"] = df["customer_name"].fillna("Unknown")
    df["sender"] = df["sender"].fillna(source)

    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")
    df["total_amount"] = (df["quantity"] * df["unit_price"]).round(2)

    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce").fillna(now)
    df["received_at"] = pd.to_datetime(df["received_at"], errors="coerce").fillna(now)
    df["ingested_at"] = now

    valid = df["product"].notna() & (df["quantity"] > 0) & (df["unit_price"] >= 0)
    bad = df[~valid]
    if not bad.empty:
        os.makedirs("data/rejected", exist_ok=True)
        path = f"data/rejected/{source}_{now:%Y%m%d_%H%M%S}.csv"
        bad.to_csv(path, index=False)
        print(f"  [{source}] {len(bad)} bad row(s) saved to {path}")
    df = df[valid].copy()

    df["source_id"] = df["source_id"].astype(str)
    df["record_id"] = [make_id(source, s) for s in df["source_id"]]
    df = df.drop_duplicates(subset="record_id", keep="last")

    df["quantity"] = df["quantity"].astype(int)
    for col in ["record_id", "source", "source_id", "sender", "customer_name", "product", "city"]:
        df[col] = df[col].astype(str)

    return df[COLUMNS]