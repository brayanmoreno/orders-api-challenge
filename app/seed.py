"""Schema and demo data.

Run directly to (re)create the local database:

    python -m app.seed --reset
"""

from __future__ import annotations

import sys

from app.db import connect, get_db_path

SCHEMA = """
CREATE TABLE IF NOT EXISTS customers (
    slug TEXT PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS orders (
    id          INTEGER PRIMARY KEY,
    customer    TEXT NOT NULL REFERENCES customers(slug),
    status      TEXT NOT NULL,
    -- Amounts arrive from the billing export as strings ("1250.00").
    amount      TEXT NOT NULL,
    created_at  TEXT NOT NULL,
    priority    INTEGER NOT NULL DEFAULT 0
);
"""

CUSTOMERS = [
    ("acme", "Acme Corp"),
    ("globex", "Globex"),
    ("initech", "Initech"),
    ("umbrella", "Umbrella"),
    ("hooli", "Hooli"),  # onboarded this week, no orders yet
]

ORDERS = [
    (1, "acme", "paid", "120.00", "2026-03-02T10:15:00", 0),
    (2, "globex", "pending", "45.50", "2026-03-05T09:00:00", 0),
    (3, "acme", "shipped", "1250.00", "2026-02-27T16:40:00", 1),
    (4, "initech", "paid", "89.90", "2026-03-07T11:20:00", 0),
    (5, "umbrella", "cancelled", "300.00", "2026-03-01T08:05:00", 0),
    (6, "globex", "paid", "8.75", "2026-03-09T14:30:00", 0),
    (7, "acme", "pending", "560.00", "2026-03-03T13:10:00", 1),
    (8, "initech", "shipped", "99.99", "2026-03-08T17:45:00", 0),
    (9, "umbrella", "paid", "1500.00", "2026-02-25T12:00:00", 1),
    (10, "globex", "shipped", "230.40", "2026-03-06T10:50:00", 0),
    (11, "acme", "paid", "75.00", "2026-03-10T09:30:00", 0),
    (12, "initech", "pending", "640.00", "2026-03-04T15:15:00", 0),
    (13, "umbrella", "paid", "50.00", "2026-03-11T18:00:00", 0),
    (14, "globex", "cancelled", "1020.00", "2026-02-28T07:45:00", 0),
    (15, "acme", "shipped", "9.90", "2026-03-12T12:25:00", 0),
]


def init_db(reset: bool = False) -> None:
    with connect() as conn:
        if reset:
            conn.executescript("DROP TABLE IF EXISTS orders; DROP TABLE IF EXISTS customers;")
        conn.executescript(SCHEMA)
        if conn.execute("SELECT COUNT(*) FROM orders").fetchone()[0] == 0:
            conn.executemany("INSERT INTO customers VALUES (?, ?)", CUSTOMERS)
            conn.executemany("INSERT INTO orders VALUES (?, ?, ?, ?, ?, ?)", ORDERS)


if __name__ == "__main__":
    init_db(reset="--reset" in sys.argv)
    print(f"Base de datos lista en {get_db_path()}")
