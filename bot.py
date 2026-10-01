import argparse
import asyncio
import logging
import os
import re
import sqlite3
import sys
from typing import Dict, List, Optional, Tuple
import pandas as pd

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

class BotDatabase:
    """
    Manages catalog data querying, price drop subscriptions, and logging.
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
            conn.commit()

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

    def search_items(self, query: str, max_price: Optional[int] = None) -> List[Dict]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            if max_price:
                cursor.execute("""
                    SELECT title, category, price, seller, in_stock 
                    FROM catalog_items
                    WHERE (title LIKE ? OR category LIKE ?) AND price <= ?
                    ORDER BY price ASC
                """, (f"%{query}%", f"%{query}%", max_price))
            else:
                cursor.execute("""
                    SELECT title, category, price, seller, in_stock 
                    FROM catalog_items
                    WHERE title LIKE ? OR category LIKE ?
                    ORDER BY price ASC
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

    def add_alert(self, user_id: int, product: str, price: int):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO price_alerts (user_id, target_product, target_price)
                VALUES (?, ?, ?)
            """, (user_id, product, price))
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

db = BotDatabase()

def parse_natural_query(user_text: str) -> Tuple[str, Optional[int]]:
    """Extracts keyword and budget filter (e.g. 'لپ تاپ زیر 40 میلیون')."""
    text = user_text.replace("میلیون", "000000").replace("هزار", "000").replace("تومان", "")
    match = re.search(r"زیر\s*([\d,]+)", text)
    max_price = None
    clean_keyword = user_text
    if match:
        num_str = match.group(1).replace(",", "").strip()
        try:
            max_price = int(num_str)
            clean_keyword = re.sub(r"زیر\s*([\d,]+|\d+)\s*(میلیون|تومان)?", "", user_text).strip()
        except ValueError:
            pass
    return clean_keyword, max_price

def format_welcome_message() -> str:
    return (
        "🤖 **به ربات هوشمند استعلام داده و بازار خوش آمدید!**\n\n"
        "دستورات و قابلیت‌های هوشمند:\n"
        "🔍 `/search <نام کالا>` - استعلام هوشمند قیمت و موجودی (پشتیبانی از فیلتر بودجه مثل: `لپ تاپ زیر ۴۰ میلیون`)\n"
        "🔔 `/alert <کالا> <قیمت>` - تنظیم هشدار افت قیمت خودکار\n"
        "📊 `/report` - گزارش آماری میانگین قیمت و موجودی انبار\n"
        "📁 **ارسال فایل اکسل یا CSV** - ممیزی خودکار داده‌ها و گزارش سلامت آماری\n"
        "ℹ️ `/help` - راهنمای سیستم"
    )

def handle_search(query: str, user_id: int = 12345) -> str:
    if not query.strip():
        return "⚠️ لطفاً نام کالا را وارد کنید. مثال: `/search لپ‌تاپ زیر ۴۰ میلیون`"
    
    clean_q, max_price = parse_natural_query(query.strip())
    results = db.search_items(clean_q, max_price=max_price)
    
    if not results:
        price_clause = f" با بودجه زیر {max_price:,} تومان" if max_price else ""
        return f"❌ موردی برای جستجوی '{clean_q}'{price_clause} یافت نشد."
    
    lines = [f"🔎 **نتایج جستجو برای '{clean_q}':** ({len(results)} مورد یافت شد)\n"]
    for idx, item in enumerate(results, 1):
        stock_badge = "✅ موجود" if item["in_stock"] else "❌ ناموجود"
        price_formatted = f"{item['price']:,} تومان"
        lines.append(
            f"{idx}. **{item['title']}**\n"
            f"   💰 قیمت: `{price_formatted}`\n"
            f"   🏢 فروشنده: {item['seller']} | {stock_badge}\n"
        )
    return "\n".join(lines)

def handle_alert(args_text: str, user_id: int = 12345) -> str:
    parts = args_text.split()
    if len(parts) < 2:
        return "⚠️ فرمت صحیح: `/alert <نام کالا> <قیمت مدنظر به تومان>`\nمثال: `/alert لپ‌تاپ 35000000`"
    try:
        price = int(''.join(filter(str.isdigit, parts[-1])))
        product = " ".join(parts[:-1])
        db.add_alert(user_id, product, price)
        return f"🔔 **هشدار قیمت با موفقیت ثبت شد!**\nبه محض افت قیمت کالا '{product}' به زیر `{price:,} تومان`، پیام دریافت خواهید کرد."
    except Exception as e:
        return f"❌ خطا در ثبت هشدار: {e}"

def handle_report(user_id: int = 12345) -> str:
    stats = db.get_summary_stats()
    return (
        "📈 **داشبورد آماری انبار و مانیتورینگ قیمت‌ها:**\n\n"
        f"📦 تعداد کل اقلام کاتالوگ: **{stats['total_items']} کالا**\n"
        f"✅ نرخ موجودی انبار: **{(stats['in_stock_items']/max(1, stats['total_items']))*100:.1f}%**\n"
        f"💵 میانگین قیمت کالاها: **{stats['avg_price']:,} تومان**\n"
        f"🕒 تاریخ گزارش: لحظه‌ای (پایگاه داده زنده)"
    )

def handle_excel_analysis(file_path: str) -> str:
    try:
        df = pd.read_excel(file_path) if file_path.endswith(".xlsx") else pd.read_csv(file_path)
        total_rows = len(df)
        cols = list(df.columns)
        null_count = df.isnull().sum().sum()
        numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
        
        summary = (
            f"📄 **گزارش جامع ممیزی فایل داده:**\n\n"
            f"• تعداد ردیف‌ها: **{total_rows:,}**\n"
            f"• تعداد ستون‌ها: **{len(cols)}**\n"
            f"• خانه‌های خالی / نامعتبر: **{null_count} مورد** (کیفیت دیتا: {100 - (null_count/(max(1, total_rows*len(cols)))*100):.1f}%)\n"
        )
        if numeric_cols:
            primary_num = numeric_cols[0]
            summary += (
                f"• میانگین ستون '{primary_num}': **{df[primary_num].mean():,.2f}**\n"
                f"• بیشینه ستون '{primary_num}': **{df[primary_num].max():,.2f}**\n"
            )
        return summary
    except Exception as e:
        return f"❌ خطا در پردازش فایل: {e}"

def run_cli_interactive():
    print("=" * 60)
    print("🤖 TELEGRAM BOT SIMULATOR (Advanced Interactive Mode)")
    print("=" * 60)
    print(format_welcome_message())
    
    while True:
        try:
            user_input = input("\nUser > ").strip()
            if not user_input:
                continue
            if user_input.lower() in ["exit", "quit", "خروج"]:
                print("خداحافظ!")
                break
            elif user_input.startswith("/start") or user_input.startswith("/help"):
                print(format_welcome_message())
            elif user_input.startswith("/search"):
                parts = user_input.split(maxsplit=1)
                q = parts[1] if len(parts) > 1 else ""
                print(handle_search(q))
            elif user_input.startswith("/alert"):
                parts = user_input.split(maxsplit=1)
                q = parts[1] if len(parts) > 1 else ""
                print(handle_alert(q))
            elif user_input.startswith("/report"):
                print(handle_report())
            else:
                print(handle_search(user_input))
        except (KeyboardInterrupt, EOFError):
            break

def main():
    parser = argparse.ArgumentParser(description="Advanced Telegram Service Bot")
    parser.add_argument("--token", default=os.getenv("BOT_TOKEN", ""), help="Telegram Bot Token")
    parser.add_argument("--test-cli", action="store_true", help="Run interactive terminal simulation")
    args = parser.parse_args()

    if args.test_cli or not args.token:
        run_cli_interactive()

if __name__ == "__main__":
    main()
