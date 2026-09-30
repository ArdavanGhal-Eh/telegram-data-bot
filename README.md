# 🤖 Telegram Data Service & Business Automation Bot

An asynchronous, lightweight Telegram bot developed in Python using `aiogram` and `SQLite`. Designed for Iranian businesses, online shops, and teams to provide instant product catalog search, inventory queries, and automated spreadsheet analytics.

---

## 🌟 Key Features
- **Instant Product Search:** Query product titles, current pricing, inventory status, and vendor names with fast SQLite full-text lookup (`/search <query>`).
- **Live Inventory & Pricing Reports:** Provides aggregate metrics on total catalog count, average market prices, and in-stock percentages (`/report`).
- **Spreadsheet Analysis:** Automated parsing and statistical summary of uploaded `.xlsx` or `.csv` files using `pandas`.
- **Zero-Dependency CLI Simulator:** Includes an interactive terminal simulation mode so anyone can evaluate the bot's conversation logic without creating a live Telegram bot.

---

## 🚀 Installation & Setup

1. **Clone repository:**
   ```bash
   git clone https://github.com/your-username/telegram-data-bot.git
   cd telegram-data-bot
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Bot Token:**
   - Copy `.env.example` to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Obtain a bot token from [@BotFather](https://t.me/BotFather) and insert it into `.env`.

---

## 💻 Usage

### 1. Run live Telegram Bot:
```bash
python bot.py --token "YOUR_TELEGRAM_BOT_TOKEN"
```

### 2. Run CLI Simulator Mode (No Token Required):
```bash
python bot.py --test-cli
```
*Try typing: `/search لپ‌تاپ`, `/report`, or `/help`*

---

## 💬 Command Reference
| دستور (Command) | کاربرد (Function) |
| :--- | :--- |
| `/start` | نمایش پیام خوش‌آمدگویی و منوی راهنما |
| `/search <کالا>` | جستجوی بلادرنگ قیمت و موجودی کالا در انبار |
| `/report` | دریافت گزارش آماری میانگین قیمت‌ها و وضعیت موجودی |
| ارسال فایل اکسل | استخراج تعداد ردیف‌ها، میانگین و بیشینه ستون‌های عددی |

---

## 🛠️ Tech Stack
- **Framework:** Python 3.10+, `aiogram` (v3)
- **Database:** `sqlite3`
- **Data Analytics:** `pandas`, `openpyxl`
- **Architecture:** Asynchronous Event-Driven Architecture

---

## 👨‍💻 Author
**Ardavan Ghal-Eh**  
Mechanical Engineering Student, Sharif University of Technology  
*Focus: Python Development, Data Pipelines & Conversational Interfaces*
