import sqlite3
from collections.abc import Iterator, Mapping
from contextlib import closing, contextmanager
from datetime import datetime
from pathlib import Path
from typing import TypedDict


DEFAULT_DB_PATH = Path(__file__).resolve().parent / "data" / "orders.db"


class OrderHistoryRow(TypedDict):
    order_id: int
    ordered_at: str
    product: str
    quantity: int
    unit_price: int
    subtotal: int
    order_total: int


@contextmanager
def _connection(db_path: Path) -> Iterator[sqlite3.Connection]:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with closing(sqlite3.connect(db_path)) as connection:
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY,
                ordered_at TEXT NOT NULL,
                total INTEGER NOT NULL CHECK (total >= 0)
            );
            CREATE TABLE IF NOT EXISTS order_items (
                id INTEGER PRIMARY KEY,
                order_id INTEGER NOT NULL REFERENCES orders(id),
                product TEXT NOT NULL,
                quantity INTEGER NOT NULL CHECK (quantity > 0),
                unit_price INTEGER NOT NULL CHECK (unit_price >= 0),
                subtotal INTEGER NOT NULL CHECK (subtotal = quantity * unit_price),
                UNIQUE (order_id, product)
            );
            """
        )
        with connection:
            yield connection


def save_order(
    cart: Mapping[str, int],
    menu: Mapping[str, int],
    db_path: Path = DEFAULT_DB_PATH,
) -> int:
    if not cart:
        raise ValueError("Cannot save an empty order.")

    items = []
    for product, quantity in cart.items():
        if product not in menu or quantity <= 0 or menu[product] < 0:
            raise ValueError("Invalid order item.")
        unit_price = menu[product]
        items.append((product, quantity, unit_price, quantity * unit_price))

    total = sum(item[3] for item in items)
    ordered_at = datetime.now().astimezone().isoformat(timespec="seconds")
    with _connection(db_path) as connection:
        cursor = connection.execute(
            "INSERT INTO orders (ordered_at, total) VALUES (?, ?)",
            (ordered_at, total),
        )
        order_id = cursor.lastrowid
        if order_id is None:
            raise sqlite3.DatabaseError("Could not obtain the saved order ID.")
        connection.executemany(
            """
            INSERT INTO order_items
                (order_id, product, quantity, unit_price, subtotal)
            VALUES (?, ?, ?, ?, ?)
            """,
            [(order_id, *item) for item in items],
        )
    return total


def load_order_history(db_path: Path = DEFAULT_DB_PATH) -> list[OrderHistoryRow]:
    with _connection(db_path) as connection:
        rows = connection.execute(
            """
            SELECT orders.id AS order_id, orders.ordered_at,
                   order_items.product, order_items.quantity,
                   order_items.unit_price, order_items.subtotal,
                   orders.total AS order_total
            FROM orders
            JOIN order_items ON order_items.order_id = orders.id
            ORDER BY orders.id DESC, order_items.id ASC
            """
        ).fetchall()
    return [
        OrderHistoryRow(
            order_id=row["order_id"],
            ordered_at=row["ordered_at"],
            product=row["product"],
            quantity=row["quantity"],
            unit_price=row["unit_price"],
            subtotal=row["subtotal"],
            order_total=row["order_total"],
        )
        for row in rows
    ]
