import logging
import os
import sqlite3
from typing import Dict, List, Optional

class BotDatabase:
    """
    Manages data querying and user logging for the Telegram Bot.
    """

    def __init__(self, db_path: str = "bot_data.db"):
        self.db_path = db_path
        self._ensure_db()

    def _get_connection(self):
        try:
            conn = sqlite3.connect(self.db_path)
            conn.execute("CREATE TABLE IF NOT EXISTS _probe (id INT)")
            return conn
        except sqlite3.OperationalError:
            self.db_path = os.path.join("/tmp", os.path.basename(self.db_path))
            return sqlite3.connect(self.db_path)

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
                CREATE TABLE IF NOT EXISTS query_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    command TEXT,
                    query TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
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
                    ("هدفون سونی WH-1000XM5", "صوتی", 19500000, "فروشگاه مرکزی", True),
                    ("ماوس لاجیتک MX Master 3S", "لوازم جانبی", 6200000, "دیجی‌کالا", False)
                ]
                cursor.executemany("""
                    INSERT INTO catalog_items (title, category, price, seller, in_stock)
                    VALUES (?, ?, ?, ?, ?)
                """, sample_data)
                conn.commit()

    def search_items(self, query: str) -> List[Dict]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT title, category, price, seller, in_stock 
                FROM catalog_items
                WHERE title LIKE ? OR category LIKE ?
            """, (f"%{query}%", f"%{query}%"))
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
