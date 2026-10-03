# 🤖 Interactive Telegram Data Service & Inventory Intelligence Bot

An asynchronous, production-grade conversational bot and data service built in **Python (`aiogram` v3)** and **SQLite**, with an optional **TypeScript edge webhook gateway**. Engineered for Iranian online stores, distributors, and warehouse teams to provide instant mobile catalog lookup, budget-aware product filtering, automated price-drop alerts, and spreadsheet quality auditing.

---

## 📌 Problem & Business Use Case
Online sellers, Instagram retail pages, and technical sales teams frequently encounter friction when customers or field staff need quick product availability, current pricing, or inventory verification. Instead of opening desktop ERP software or browsing complex dashboards:
1. Users send natural language queries directly on Telegram (e.g., *«لپ‌تاپ زیر ۴۰ میلیون»*).
2. The bot parses budget limits and keywords, queries a live SQLite database, and returns formatted price and availability badges.
3. Users can set target price alerts (`/alert`) to receive notifications when supplier pricing drops.
4. Managers can upload `.xlsx` or `.csv` files directly in chat to receive an instant statistical data health report.

---

## 🌟 System Architecture

```text
┌──────────────────────────────────────┐
│       User / Customer on Telegram    │
└──────────────────┬───────────────────┘
                   │ Updates (Webhook / Polling)
                   ▼
┌──────────────────────────────────────┐
│  TypeScript Gateway (Optional Edge)  │ ───> Microsecond ACK & Ingestion
└──────────────────┬───────────────────┘
                   │
                   ▼
┌──────────────────────────────────────┐
│   Python Asynchronous Bot (aiogram)  │
└──────────────────┬───────────────────┘
                   │
         ┌─────────┴─────────┬────────────────────────┐
         ▼                   ▼                        ▼
┌─────────────────┐ ┌─────────────────┐ ┌───────────────────────────┐
│ Natural Language│ │  SQLite Storage │ │  In-Chat Excel Auditor    │
│ Budget Parser   │ │  - Catalog      │ │  (Pandas Missing Values,   │
│ (Regex & NLP)   │ │  - Price Alerts │ │   Averages, Distributions) │
└─────────────────┘ └─────────────────┘ └───────────────────────────┘
```

---

## 🔑 Key Engineering Features

- **Natural Language Budget Extraction:** Automatically parses conversational Persian phrases like *«زیر ۴۰ میلیون»* or *«کمتر از ۱۵ تومن»*, separating the item keyword from the numeric price threshold.
- **Automated Price Drop Alert System:** Users subscribe to target thresholds via `/alert <کالا> <قیمت>`, stored in the `price_alerts` table for event-driven push notifications.
- **In-Chat Spreadsheet Auditing:** When an Excel or CSV file is dragged into the chat, the bot parses it with `pandas`, calculates total rows, missing/null value percentages, and key column metrics (mean, max, distribution).
- **Zero-Dependency CLI Simulator (`--test-cli`):** Includes a complete interactive terminal simulation mode so recruiters, evaluators, or developers can test all commands without needing an active Telegram BotFather token.
- **Polyglot TypeScript Gateway (`typescript_webhook_gateway/`):** Optional Express.js/TypeScript edge receiver for zero-cold-start cloud webhook deployment.

---

## 💬 Command Reference

| دستور (Command) | نحوه استفاده (Usage) | توضیح عملکرد (Description) |
| :--- | :--- | :--- |
| `/start` | `/start` | نمایش منوی تعاملی و پیام خوش‌آمدگویی |
| `/search` | `/search لپ‌تاپ زیر ۴۰ میلیون` | جستجوی بلادرنگ محصولات با فیلتر هوشمند سقف قیمت |
| `/alert` | `/alert مک‌بوک 85000000` | ثبت هشدار برای اطلاع‌رسانی خودکار در صورت کاهش قیمت |
| `/report` | `/report` | صدور گزارش تحلیلی میانگین قیمت‌ها و درصد موجودی انبار |
| **ارسال فایل** | بارگذاری فایل `.xlsx` یا `.csv` | بررسی صحت داده‌ها، شمارش داده‌های تهی (Null) و استخراج شاخص‌ها |
| `/help` | `/help` | مشاهده راهنمای دستورات و مثال‌های کاربردی |

---


---

## 📄 Module 4: Official Commercial Pro-Forma Invoice Generator ()
- **Automated In-Chat PDF Issuance:** Generates professional A4 pro-forma invoices directly within the conversation.
- **Commercial Tax & VAT Compliance:** Computes subtotals, standard 0\%$ Iranian VAT (مالیات بر ارزش افزوده), and net grand totals in Toman.
- **Standardized Enterprise Layout:** Includes invoice serialization, buyer/seller economic IDs, validity periods, and digital verification footer.
- **Quick Run:**
  

## 🚀 Installation & Setup

### 1. Clone Repository
```bash
git clone https://github.com/ArdavanGhal-Eh/telegram-data-bot.git
cd telegram-data-bot
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run in Interactive CLI Simulator (No Token Required):
```bash
python bot.py --test-cli
```
*Try typing: `/search لپ‌تاپ`, `/search گوشی زیر ۲۰ میلیون`, or `/report`*

### 4. (Optional) Run Live Telegram Bot:
1. Get a bot token from [@BotFather](https://t.me/BotFather) on Telegram.
2. Run the bot:
   ```bash
   python bot.py --token "YOUR_TELEGRAM_BOT_TOKEN_HERE"
   ```

### 5. (Optional) Launch TypeScript Webhook Gateway:
```bash
cd typescript_webhook_gateway
npm install
npm start
```

---

## 🛠️ Tech Stack
- **Bot Engine:** Python 3.10+, `aiogram` (v3 async framework)
- **Database:** `sqlite3` (Full-Text Search & Persistence)
- **Data Analytics:** `pandas`, `openpyxl`
- **Edge Gateway:** TypeScript, Node.js, Express

---

## 👨‍💻 Author
**Ardavan Ghal-Eh**  
Mechanical Engineering Student, Sharif University of Technology  
*Focus: Conversational Systems, Data Engineering & Automation*
