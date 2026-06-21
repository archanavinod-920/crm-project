import sqlite3

conn = sqlite3.connect("beautycrm.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS customers(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    phone TEXT,
    email TEXT,
    gender TEXT,
    skin_type TEXT,
    address TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS purchase_history(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER,
    product_name TEXT,
    quantity INTEGER,
    amount REAL,
    purchase_date TEXT
)
""")

cursor.execute("""
INSERT INTO purchase_history
(customer_id, product_name, quantity, amount, purchase_date)
VALUES (?, ?, ?, ?, ?)
""",
(6, "Minimalist Face wash", 2, 500, "2026-06-17"))

cursor.execute("""
CREATE TABLE IF NOT EXISTS customer_registration(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    phone TEXT,
    email TEXT,
    dob TEXT,
    gender TEXT,
    skin_type TEXT,
    category TEXT,
    address TEXT,
    password TEXT
)
""")

cursor.execute("""
            create table if not exists products(
            id text,
            category text,
            product text,
            price integer,
            qty integer
        )
""")

conn.commit()
conn.close()


