import json
import os
import sqlite3

import pandas as pd

STATE_FILE = "data/state.json"  


def load_state():
    if os.path.exists(STATE_FILE):
        return json.load(open(STATE_FILE))
    return {}


def save_state(state):
    json.dump(state, open(STATE_FILE, "w"), indent=2)


def fetch_from_db():
    last = load_state().get("db_last_updated_at", "1970-01-01 00:00:00")

    conn = sqlite3.connect("data/client_db.sqlite")
    df = pd.read_sql(
        "SELECT * FROM orders WHERE updated_at > ? ORDER BY updated_at",
        conn,
        params=(last,),
    )
    conn.close()

    new_last = df["updated_at"].max() if not df.empty else None
    df["sender"] = "client_database"
    return df, new_last


if __name__ == "__main__":
    df, new_last = fetch_from_db()
    print(f"Fetched {len(df)} new orders")
    print(df.head())