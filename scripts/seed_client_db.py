import random
import sqlite3
from datetime import datetime, timedelta

PRODUCTS = {
    "Tomato Seeds": 150,
    "Organic Fertilizer": 320,
    "Drip Irrigation Kit": 1250,
    "Cucumber Seeds": 120,
    "Pesticide Spray": 210,
}
CITIES = ["Cairo", "Giza", "Alexandria", "Mansoura", "Tanta"]
NAMES = ["Ahmed Ali", "Mona Hassan", "Omar Khaled", "Sara Adel", "Youssef Samir"]

conn = sqlite3.connect("data/client_db.sqlite")

conn.execute("""
CREATE TABLE IF NOT EXISTS orders (
    order_id   TEXT PRIMARY KEY,
    customer   TEXT,
    product    TEXT,
    qty        INTEGER,
    price      REAL,
    city       TEXT,
    created_at TEXT,
    updated_at TEXT
)
""")

count = conn.execute("SELECT COUNT(*) FROM orders").fetchone()[0]

now = datetime.now()
for i in range(20):  
    product = random.choice(list(PRODUCTS))
    conn.execute(
        "INSERT INTO orders VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (
            f"DB-{count + i + 1:05d}",            
            random.choice(NAMES),
            product,
            random.randint(1, 20),                     
            PRODUCTS[product],                         
            random.choice(CITIES),
            (now - timedelta(days=random.randint(0, 30))).strftime("%Y-%m-%d %H:%M:%S"),
            now.strftime("%Y-%m-%d %H:%M:%S.%f"),       
        ),
    )

conn.commit()
total = conn.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
print(f"Added 20 orders. Total orders now: {total}")
conn.close()