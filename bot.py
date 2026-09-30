import argparse
import asyncio
import logging
import os
import sqlite3
import sys
from typing import Dict, List, Optional
import pandas as pd

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

class BotDatabase:
    """
    Manages catalog data querying, logging, and metrics for the Telegram Bot.
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

db = BotDatabase()

def format_welcome_message() -> str:
    return (
        "🤖 **به ربات دستیار استعلام داده و بازار خوش آمدید!**\n\n"
        "دستورات در دسترس:\n"
        "🔍 `/search <نام کالا>` - استعلام قیمت و وضعیت موجودی\n"
        "📊 `/report` - گزارش آماری میانگین قیمت و موجودی انبار\n"
        "📁 **ارسال فایل اکسل یا CSV** - تحلیل خودکار داده‌ها و صدور خلاصه گزارش\n"
        "ℹ️ `/help` - راهنمای سیستم"
    )

def handle_search(query: str, user_id: int = 12345) -> str:
    if not query.strip():
        return "⚠️ لطفاً نام کالا را پس از دستور وارد کنید. مثال: `/search لپ‌تاپ`"
    
    db.log_query(user_id=user_id, command="search", query=query)
    results = db.search_items(query.strip())
    
    if not results:
        return f"❌ موردی برای جستجوی '{query}' یافت نشد."
    
    lines = [f"🔎 **نتایج جستجو برای '{query}':** ({len(results)} مورد)\n"]
    for idx, item in enumerate(results, 1):
        stock_badge = "✅ موجود" if item["in_stock"] else "❌ ناموجود"
        price_formatted = f"{item['price']:,} تومان"
        lines.append(
            f"{idx}. **{item['title']}**\n"
            f"   💰 قیمت: `{price_formatted}`\n"
            f"   🏢 فروشنده: {item['seller']} | {stock_badge}\n"
        )
    return "\n".join(lines)

def handle_report(user_id: int = 12345) -> str:
    db.log_query(user_id=user_id, command="report")
    stats = db.get_summary_stats()
    return (
        "📈 **گزارش آماری موجودی و قیمت‌های سیستم:**\n\n"
        f"📦 تعداد کل اقلام کاتالوگ: **{stats['total_items']} عدد**\n"
        f"✅ اقلام دارای موجودی: **{stats['in_stock_items']} عدد**\n"
        f"💵 میانگین قیمت کالاها: **{stats['avg_price']:,} تومان**\n"
        f"🕒 تاریخ گزارش: لحظه‌ای (پایگاه داده زنده)"
    )

def handle_excel_analysis(file_path: str) -> str:
    try:
        df = pd.read_excel(file_path) if file_path.endswith(".xlsx") else pd.read_csv(file_path)
        total_rows = len(df)
        cols = list(df.columns)
        numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
        
        summary = (
            f"📄 **تحلیل فایل داده انجام شد:**\n\n"
            f"• تعداد ردیف‌ها: **{total_rows}**\n"
            f"• تعداد ستون‌ها: **{len(cols)}**\n"
            f"• ستون‌ها: `{', '.join(cols[:5])}`...\n"
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
    print("🤖 TELEGRAM BOT SIMULATOR (CLI Interactive Mode)")
    print("=" * 60)
    print(format_welcome_message())
    print("\n[تست تعاملی فعال است. دستوراتی مثل /search لپ‌تاپ یا /report یا exit را وارد کنید]")
    
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
            elif user_input.startswith("/report"):
                print(handle_report())
            else:
                print(handle_search(user_input))
        except (KeyboardInterrupt, EOFError):
            break

async def start_telegram_polling(token: str):
    try:
        from aiogram import Bot, Dispatcher, types
        from aiogram.filters import Command
    except ImportError:
        logging.error("aiogram is not installed. Please run: pip install aiogram")
        return

    bot = Bot(token=token)
    dp = Dispatcher()

    @dp.message(Command("start"))
    async def cmd_start(message: types.Message):
        await message.answer(format_welcome_message(), parse_mode="Markdown")

    @dp.message(Command("search"))
    async def cmd_search(message: types.Message):
        args = message.text.split(maxsplit=1)
        query = args[1] if len(args) > 1 else ""
        response = handle_search(query, user_id=message.from_user.id)
        await message.answer(response, parse_mode="Markdown")

    @dp.message(Command("report"))
    async def cmd_report(message: types.Message):
        response = handle_report(user_id=message.from_user.id)
        await message.answer(response, parse_mode="Markdown")

    @dp.message()
    async def general_handler(message: types.Message):
        if message.text:
            response = handle_search(message.text, user_id=message.from_user.id)
            await message.answer(response, parse_mode="Markdown")

    logging.info("Starting Telegram Bot Polling...")
    await dp.start_polling(bot)

def main():
    parser = argparse.ArgumentParser(description="Telegram Data Service & Automation Bot")
    parser.add_argument("--token", default=os.getenv("BOT_TOKEN", ""), help="Telegram Bot Token from BotFather")
    parser.add_argument("--test-cli", action="store_true", help="Run interactive terminal simulation")
    args = parser.parse_args()

    if args.test_cli or not args.token:
        if not args.token and not args.test_cli:
            logging.info("No BOT_TOKEN provided in environment. Automatically starting in CLI Simulation mode.")
        run_cli_interactive()
    else:
        asyncio.run(start_telegram_polling(args.token))

if __name__ == "__main__":
    main()
