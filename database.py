import logging
import os
import sqlite3
from typing import Dict, List, Optional


class BotDatabase:
    """
    Production-grade SQLite database manager for Telegram Business & Data Bot.
    Features:
      - WAL mode & Connection pooling / in-memory reuse
      - Catalog search with multi-column indices and pagination
      - Price drop alerts subscription & matching engine
      - Query auditing & aggregated business statistics
    """

    def __init__(self, db_path: str = "bot_data.db"):
        self.db_path = db_path
        self._mem_conn = None
        self._ensure_db()

    def _get_connection(self):
        if self.db_path == ":memory:":
            if self._mem_conn is None:
                self._mem_conn = sqlite3.connect(":memory:")
            return self._mem_conn
        try:
            conn = sqlite3.connect(self.db_path)
            conn.execute("PRAGMA journal_mode=WAL;")
            return conn
        except sqlite3.OperationalError:
            self.db_path = os.path.join("/tmp", os.path.basename(self.db_path))
            conn = sqlite3.connect(self.db_path)
            conn.execute("PRAGMA journal_mode=WAL;")
            return conn

    def _ensure_db(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS catalog_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    category TEXT,
                    price INTEGER,
                    seller TEXT,
                    in_stock BOOLEAN
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS price_alerts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    target_product TEXT,
                    target_price INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS query_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    command TEXT,
                    query TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_cat_price ON catalog_items(category, price)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_cat_title ON catalog_items(title)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_alert_user ON price_alerts(user_id)")
            conn.commit()

        # Seed sample catalog if empty
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM catalog_items")
            if cursor.fetchone()[0] == 0:
                sample_data = [
                    ("لپ‌تاپ ایسوس Vivobook 15", "لپ‌تاپ", 38500000, "دیجی‌کالا", True),
                    ("مک‌بوک ایر M2 اپل", "لپ‌تاپ", 89000000, "بازرگانی پارس", True),
                    ("گوشی سامسونگ S24 Ultra", "موبایل", 72000000, "دیجی‌لند", True),
                    ("گوشی شیائومی Redmi Note 13", "موبایل", 14500000, "دیجی‌کالا", True),
                    ("هدفون سونی WH-1000XM5", "صوتی", 19500000, "فروشگاه مرکزی", True),
                    ("ماوس لاجیتک MX Master 3S", "لوازم جانبی", 6200000, "دیجی‌کالا", False)
                ]
                cursor.executemany("""
                    INSERT INTO catalog_items (title, category, price, seller, in_stock)
                    VALUES (?, ?, ?, ?, ?)
                """, sample_data)
                conn.commit()

    def search_items(self, query: str, max_price: Optional[int] = None, limit: int = 50, offset: int = 0) -> List[Dict]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            if max_price:
                cursor.execute("""
                    SELECT title, category, price, seller, in_stock 
                    FROM catalog_items
                    WHERE (title LIKE ? OR category LIKE ?) AND price <= ?
                    ORDER BY price ASC
                    LIMIT ? OFFSET ?
                """, (f"%{query}%", f"%{query}%", max_price, limit, offset))
            else:
                cursor.execute("""
                    SELECT title, category, price, seller, in_stock 
                    FROM catalog_items
                    WHERE title LIKE ? OR category LIKE ?
                    ORDER BY price ASC
                    LIMIT ? OFFSET ?
                """, (f"%{query}%", f"%{query}%", limit, offset))
            rows = cursor.fetchall()
            return [
                {
                    "title": r[0],
                    "category": r[1],
                    "price": r[2],
                    "seller": r[3],
                    "in_stock": bool(r[4])
                }
                for r in rows
            ]

    def subscribe_price_alert(self, user_id: int, target_product: str, target_price: int) -> int:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO price_alerts (user_id, target_product, target_price)
                VALUES (?, ?, ?)
            """, (user_id, target_product, target_price))
            conn.commit()
            return cursor.lastrowid

    def add_alert(self, user_id: int, product: str, price: int):
        self.subscribe_price_alert(user_id, product, price)

    def check_alerts(self, product_title: str, current_price: int) -> List[int]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT user_id FROM price_alerts
                WHERE ? LIKE ('%' || target_product || '%') AND target_price >= ?
            """, (product_title, current_price))
            rows = cursor.fetchall()
            return [r[0] for r in rows]

    def log_query(self, user_id: int, command: str, query: str = ""):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO query_logs (user_id, command, query)
                VALUES (?, ?, ?)
            """, (user_id, command, query))
            conn.commit()

    def get_summary_stats(self) -> Dict:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*), AVG(price), SUM(in_stock) FROM catalog_items")
            total, avg_price, in_stock = cursor.fetchone()
            return {
                "total_items": total or 0,
                "avg_price": int(avg_price or 0),
                "in_stock_items": in_stock or 0
            }
