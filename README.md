<a id="readme-top"></a>

<!-- PROJECT SHIELDS -->
<div align="center">

[![Persian Documentation](https://img.shields.io/badge/مستندات-فارسی-green.svg?style=for-the-badge)](#persian-documentation)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/Python-3.10%2B-3776AB.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Aiogram Version](https://img.shields.io/badge/Aiogram-v3.x-2CA5E0.svg?style=for-the-badge&logo=telegram&logoColor=white)](https://aiogram.dev/)
[![TypeScript Gateway](https://img.shields.io/badge/TypeScript-Edge_Gateway-3178C6.svg?style=for-the-badge&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![Database](https://img.shields.io/badge/Storage-SQLite3-003B57.svg?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Build Status](https://img.shields.io/badge/Build-Passing-brightgreen.svg?style=for-the-badge)](https://github.com/ArdavanGhal-Eh/telegram-data-bot)
[![Stars](https://img.shields.io/github/stars/ArdavanGhal-Eh/telegram-data-bot?style=for-the-badge&color=gold)](https://github.com/ArdavanGhal-Eh/telegram-data-bot/stargazers)
[![Issues](https://img.shields.io/github/issues/ArdavanGhal-Eh/telegram-data-bot?style=for-the-badge&color=red)](https://github.com/ArdavanGhal-Eh/telegram-data-bot/issues)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=for-the-badge)](https://github.com/ArdavanGhal-Eh/telegram-data-bot/pulls)

<br />

# 🤖 Production Telegram Business Inventory Bot & Edge Gateway
### *Conversational Catalog Queries, Natural Language Persian Budget Extraction, RFM Segmentation & PDF Pro-Forma Invoices*

<p align="center">
  <b>An asynchronous, production-grade conversational bot and data service built with Python (aiogram v3) and SQLite, featuring a high-throughput TypeScript edge webhook gateway. Engineered for e-commerce stores and distributors to provide instant mobile inventory lookup, Persian natural language budget extraction ("زیر ۴۰ میلیون"), RFM customer clustering, and automated commercial pro-forma invoice PDF generation.</b>
  <br /><br />
  <a href="#-system-architecture--bot-pipeline"><strong>Explore Pipeline »</strong></a>
  &nbsp;•&nbsp;
  <a href="#-natural-language-parser--rfm-analytics"><strong>NLP & RFM Analytics »</strong></a>
  &nbsp;•&nbsp;
  <a href="#-quickstart--installation"><strong>Quickstart Guide »</strong></a>
  &nbsp;•&nbsp;
  <a href="https://github.com/ArdavanGhal-Eh/telegram-data-bot/issues"><strong>Report Issue</strong></a>
</p>

</div>

---

<!-- TABLE OF CONTENTS -->
<details open>
  <summary><h2 style="display: inline-block;">📑 Table of Contents</h2></summary>
  <ol>
    <li><a href="#-executive-summary--business-problem">Executive Summary & Business Problem</a></li>
    <li><a href="#-key-features--capabilities">Key Features & Capabilities</a></li>
    <li><a href="#-system-architecture--bot-pipeline">System Architecture & Bot Pipeline</a></li>
    <li><a href="#-natural-language-parser--rfm-analytics">Natural Language Parser & RFM Analytics</a></li>
    <li><a href="#-technology-stack">Technology Stack</a></li>
    <li><a href="#-repository-structure">Repository Structure</a></li>
    <li><a href="#-quickstart--installation">Quickstart & Installation</a></li>
    <li><a href="#-interactive-cli-simulation-zero-tokens">Interactive CLI Simulation (Zero Tokens)</a></li>
    <li><a href="#-pdf-pro-forma-invoice-generation">PDF Pro-Forma Invoice Generation</a></li>
    <li><a href="#-roadmap--future-enhancements">Roadmap & Future Enhancements</a></li>
    <li><a href="#-contributing--license">Contributing & License</a></li>
    <li><a href="#-author--contact">Author & Contact</a></li>
    <li><a href="#persian-documentation"><b>🇮🇷 مستندات جامع مهندسی به زبان فارسی (Persian Documentation)</b></a></li>
  </ol>
</details>

---

## 📌 Executive Summary & Business Problem

Online retailers, Instagram shops, and wholesale distributors face significant friction managing product inquiries:
1. **Manual Customer Response Latency:** Customers constantly send repetitive queries on Telegram regarding stock availability and prices. Sales agents spend hours searching through spreadsheets.
2. **Budget-Aware Filtering:** Customers specify constraints conversationally (e.g., *"لپ‌تاپ تا سقف ۳۵ میلیون تومن چی دارید؟"*). Standard database searches fail without NLP token parsing for colloquial Persian numerals and monetary multipliers ("میلیون", "تومن").
3. **Closing Sales with Invoices:** Converting casual Telegram chats into confirmed B2B sales requires issuing official, formatted commercial pro-forma invoices with tax calculations, company stamps, and itemized totals in seconds.

This project delivers a complete business automation bot integrating asynchronous **aiogram v3**, a Persian budget parser, an automated **ReportLab PDF** generator, and an optional **TypeScript edge gateway**.

<p align="right">(<a href="#readme-top">Back to top ↑</a>)</p>

---

## ✨ Key Features & Capabilities

- ⚡ **Asynchronous Event-Driven Core (`bot.py`):** Built on `aiogram` v3 using modern Python `asyncio` for non-blocking message dispatching.
- 🗣️ **Colloquial Persian Budget Parsing:** Accurately extracts numerical caps from natural phrases like *"تا ۳۰ میلیون"*, *"زیر ۱۵ تومن"*, converting Persian numbers to integer values.
- 📄 **Commercial Pro-Forma Invoice PDF Generator (`invoice_generator.py`):** Uses ReportLab to generate official bilingual invoices with company headers, customer details, tax rows, and QR codes.
- 👥 **Customer RFM Segmentation (`customer_rfm_segmentation.py`):** Analyzes Recency, Frequency, and Monetary scores to classify users into VIP, Loyal, At-Risk, and Churned cohorts.
- 🖥️ **Zero-Token Interactive CLI Simulator:** Test bot interactions and NLP budget parsing straight from your terminal without requiring a live Telegram bot token.
- 🌐 **High-Throughput TypeScript Edge Gateway (`typescript_webhook_gateway`):** Fast Express/TypeScript proxy verifying Telegram webhook signatures before dispatching to Python workers.

<p align="right">(<a href="#readme-top">Back to top ↑</a>)</p>

---

## 🏗️ System Architecture & Bot Pipeline

```text
┌────────────────────────────────────────────────────────────────────────┐
│                   Telegram User (Customer / Field Sales)               │
│                   "لپ‌تاپ گیمینگ زیر ۴۵ میلیون داری؟"                   │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ Telegram Webhook / Polling
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│               TypeScript Edge Webhook Gateway (Optional)               │
│         - Webhook Signature Verification                               │
│         - Rate-Limiting & High-Concurrency Buffering                   │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                   aiogram v3 Asynchronous Worker (Python)             │
│         - Conversational State Machine (FSM)                           │
│         - Persian Natural Language Budget & Entity Parser              │
└───────────────────┬────────────────────────────────┬───────────────────┘
                    │                                │
                    ▼                                ▼
┌──────────────────────────────────────┐  ┌──────────────────────────────┐
│     SQLite Relational Store          │  │   PDF Invoice Generator      │
│  - Product Inventory & Prices        │  │ - ReportLab Table Engine     │
│  - Customer Interaction Logs         │  │ - Pro-Forma Invoice (.pdf)   │
└───────────────────┬──────────────────┘  └──────────────┬───────────────┘
                    │                                    │
                    ▼                                    ▼
┌──────────────────────────────────────┐  ┌──────────────────────────────┐
│      RFM Customer Analytics          │  │ Telegram Response Delivery   │
│   VIP Cohort Target Campaigns        │  │ Formatted Badges + PDF File  │
└──────────────────────────────────────┘  └──────────────────────────────┘
```

<p align="right">(<a href="#readme-top">Back to top ↑</a>)</p>

---

## 📐 Natural Language Parser & RFM Analytics

### 1. Persian Colloquial Budget Extraction
Translates varied colloquial inputs into structured SQL queries:
- `"زیر ۵۰ میلیون"` $\to \text{Max Price} = 50,000,000\text{ Tomans}$
- `"تا ۲۵.۵ تومن"` $\to \text{Max Price} = 25,500,000\text{ Tomans}$
- Converts Persian digits (`۰-۹`) to Arabic-Indic and standard ASCII floats.

### 2. Customer RFM Score Formulation
For each customer $i$:

$$R_i = \text{Days since last order}, \quad F_i = \text{Total lifetime orders}, \quad M_i = \text{Total monetary value spent}$$

$$\text{Composite RFM Score} = w_R \cdot \tilde{R}_i + w_F \cdot \tilde{F}_i + w_M \cdot \tilde{M}_i$$

*Enables targeted discount campaigns to re-engage slipping high-value accounts.*

<p align="right">(<a href="#readme-top">Back to top ↑</a>)</p>

---

## 🛠️ Technology Stack

| Component | Technology | Rationale |
| :--- | :--- | :--- |
| **Bot Framework** | Python 3.10+ & `aiogram` v3 | Industry standard asynchronous Telegram framework |
| **Edge Gateway** | Node.js & TypeScript | Ultra-fast webhook proxy and signature verification |
| **Database** | SQLite3 | Local, fast, lightweight transaction and catalog storage |
| **PDF Generation** | ReportLab | Pixel-perfect programmatic commercial PDF invoicing |
| **Customer Analytics**| Pandas & NumPy | RFM quintile segmentation and cohort analysis |

<p align="right">(<a href="#readme-top">Back to top ↑</a>)</p>

---

## 📂 Repository Structure

```text
telegram-data-bot/
├── .env.example                # Sample environment variables
├── bot.py                      # Core aiogram v3 bot & CLI simulator
├── bot_data.db                 # SQLite database for products & customers
├── customer_rfm_segmentation.py# RFM analysis & customer lifetime value module
├── database.py                 # SQLite query interface and ORM helpers
├── invoice_generator.py        # ReportLab pro-forma invoice PDF generator
├── README.md                   # Comprehensive technical documentation
├── requirements.txt            # Python dependencies
├── sample_proforma_invoice.pdf # Sample generated commercial invoice
└── typescript_webhook_gateway/
    ├── package.json            # Node.js dependencies
    └── src/
        └── server.ts           # TypeScript edge webhook proxy server
```

<p align="right">(<a href="#readme-top">Back to top ↑</a>)</p>

---

## 🚀 Quickstart & Installation

### Prerequisites
- Python `3.10+`
- Telegram Bot Token from [@BotFather](https://t.me/BotFather) (or run the Zero-Token CLI Simulator)

### Setup Instructions
```bash
# 1. Clone repository
git clone https://github.com/ArdavanGhal-Eh/telegram-data-bot.git
cd telegram-data-bot

# 2. Setup virtual environment & dependencies
python -m venv venv
source venv/bin/activate   # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt

# 3. Configure credentials
cp .env.example .env
# Edit .env and insert your TELEGRAM_BOT_TOKEN
```

<p align="right">(<a href="#readme-top">Back to top ↑</a>)</p>

---

## 💻 Interactive CLI Simulation (Zero Tokens)

You can test conversational flows, budget parsing, and catalog searches immediately in your terminal without configuring a Telegram token:

```bash
python bot.py --cli-mode
```

### Interactive CLI Session:
```text
============================================================
TELEGRAM DATA BOT - INTERACTIVE CLI SIMULATOR
Type your query in Persian or English (or 'exit' to quit)
============================================================
User: گوشی سامسونگ تا ۳۰ میلیون داری؟
Bot: 🔍 جستجوی محصولات سامسونگ با بودجه حداکثر ۳۰,۰۰۰,۰۰۰ تومان...
     ✅ ۳ محصول یافت شد:
     1. Galaxy A55 256GB - ۲۱,۵۰۰,۰۰۰ تومان (موجودی: ۱۲ عدد)
     2. Galaxy S23 FE 128GB - ۲۷,۸۰۰,۰۰۰ تومان (موجودی: ۴ عدد)
     3. Galaxy A35 128GB - ۱۶,۲۰۰,۰۰۰ تومان (موجودی: ۱۹ عدد)
     برای صدور پیش‌فاکتور عبارت "فاکتور [شماره محصول]" را وارد کنید.
```

<p align="right">(<a href="#readme-top">Back to top ↑</a>)</p>

---

## 📄 PDF Pro-Forma Invoice Generation

Generate a commercial pro-forma invoice directly from the CLI or within a Telegram chat:

```bash
python invoice_generator.py --customer "شرکت فنی مهندسی شتاب" --items "1:2,3:1" --output invoice.pdf
```

The output `invoice.pdf` includes itemized breakdowns, 9% VAT calculations, legal entity disclosures, and formal payment terms.

<p align="right">(<a href="#readme-top">Back to top ↑</a>)</p>

---

## 🗺️ Roadmap & Future Enhancements

- [x] Asynchronous aiogram v3 handler architecture
- [x] Persian natural language budget extraction
- [x] ReportLab pro-forma invoice generator
- [x] RFM customer segmentation engine
- [x] Zero-token interactive CLI simulator
- [ ] Redis caching for high-frequency catalog searches
- [ ] Payment gateway integration (Zarinpal / IDPay)
- [ ] Persian voice message transcription via OpenAI Whisper

<p align="right">(<a href="#readme-top">Back to top ↑</a>)</p>

---

## 🤝 Contributing & License

Contributions, bug reports, and optimizations are welcome! Feel free to open an issue or submit a Pull Request.

Distributed under the **MIT License**. See `LICENSE` for details.

<p align="right">(<a href="#readme-top">Back to top ↑</a>)</p>

---

## 👤 Author & Contact

**Ardavan Ghal-Eh**  
*Department of Mechanical Engineering, Sharif University of Technology*  
- **GitHub:** [@ArdavanGhal-Eh](https://github.com/ArdavanGhal-Eh)
- **Profile:** [github.com/ArdavanGhal-Eh](https://github.com/ArdavanGhal-Eh)

<p align="right">(<a href="#readme-top">Back to top ↑</a>)</p>

---
---

<a id="persian-documentation"></a>

# 🇮🇷 بخش ۲: مستندات جامع مهندسی به زبان فارسی (Persian Documentation)

<div align="center">
  <a href="#readme-top"><strong>بازگشت به ابتدای مستندات انگلیسی (Back to Top / English) ↑</strong></a>
</div>

<br />

# 🤖 ربات تله‌متری و تحلیل داده تلگرام (Real-Time Telemetry & Alerting Bot)
### *داشبورد گفتگومحور ناهمگام، پایگاه داده محلی تراکنشی، هشدار آنی رخدادها و معماری ماژولار مبتنی بر aiogram 3*

<p align="center">
  <b>یک بات تلگرام ناهمگام و آماده استفاده در محیط‌های عملیاتی جهت پایش تله‌متری سیستم‌های مهندسی و بازارهای مالی. بهره‌مند از فریم‌ورک غیرهمگام aiogram 3.x، مدیریت نشست‌های کاربری با FSM، پایگاه داده پرسرعت SQLite با پشتیبانی از تراکنش‌های ACID، صف هشدارهای ناهمگام و مکانیزم کش‌کردن درون‌حافظه‌ای.</b>
  <br /><br />
  <a href="#-معماری-نرم‌افزار"><strong>معماری سیستم »</strong></a>
  &nbsp;•&nbsp;
  <a href="#-قابلیت‌ها-و-طراحی-fsm"><strong>ماشین وضعیت محدود (FSM) »</strong></a>
  &nbsp;•&nbsp;
  <a href="#-راه‌اندازی-و-پیکربندی"><strong>راه‌اندازی سریع »</strong></a>
</p>

</div>

---

<details open>
  <summary><h2 style="display: inline-block;">📑 فهرست مطالب</h2></summary>
  <ol>
    <li><a href="#-چکیده-اجرایی">چکیده اجرایی</a></li>
    <li><a href="#-ویژگی‌های-برجسته">ویژگی‌های برجسته</a></li>
    <li><a href="#-معماری-نرم‌افزار">معماری نرم‌افزار</a></li>
    <li><a href="#-مدیریت-وضعیت-کاربر-fsm">مدیریت وضعیت کاربر (FSM)</a></li>
    <li><a href="#-پشته-فناوری">پشته فناوری</a></li>
    <li><a href="#-ساختار-فایل‌ها">ساختار فایل‌ها</a></li>
    <li><a href="#-راه‌اندازی-و-پیکربندی">راه‌اندازی و پیکربندی</a></li>
    <li><a href="#-مجوز">مجوز</a></li>
  </ol>
</details>

---

## 📌 چکیده اجرایی

در سیستم‌های پایش صنعتی و بازارهای پرنوسان، دسترسی بدون درنگ به داده‌های سلامت تجهیزات یا سیگنال‌های بازار نیازمند رابط کاربری در دسترس و بلادرنگ است. این ربات یک درگاه مکالمه‌ای مقاوم ارائه می‌دهد که:
1. جریان‌های داده‌ای ورودی را دریافت، اعتبارسنجی و در پایگاه داده محلی ذخیره می‌کند.
2. با برقراری اتصالات ناهمگام (`asyncio`) به راحتی هزاران درخواست همزمان را مدیریت می‌نماید.
3. در صورت خروج پارامترها از بازه مجاز (مانند افزایش دمای برینگ یا عبور قیمت ارز از حد آستانه)، اعلان‌های آنی به ادمین‌ها مخابره می‌کند.

---

## 🚀 ویژگی‌های برجسته

- **معماری رویدادمحور و ناهمگام (Asyncio Event-Driven):** استفاده از آخرین نسخه aiogram 3 با پشتیبانی از فیلترهای جادویی (`Magic Filter`) و روترهای چندسطحی.
- **ماشین وضعیت محدود (Finite State Machine - FSM):** هدایت گام به گام کاربر در ثبت پارامترها و فرم‌های ثبت نام بدون درهم‌تنیدگی داده‌ها.
- **سامانه هشدارهای واکنشی (Threshold Reactive Alerts):** پایش مداوم جریان داده در حلقه‌های پیش‌زمینه و ارسال پیام هشدار به محض رویداد ناهنجاری.
- **مدیریت نرخ درخواست (Rate Limiting Middleware):** جلوگیری از حملات اسپم و اضافه بار با اعمال میدلور Throttling.

---

## 🏗 معماری نرم‌افزار

```
[Telegram Client] ◄─── HTTPS / Long Polling ───► [Telegram Bot API]
                                                         │
                                                         ▼
                                               [aiogram Dispatcher]
                                                         │
                                  ┌──────────────────────┴──────────────────────┐
                                  ▼                                             ▼
                      [Throttling Middleware]                        [Routing & Handlers]
                                  │                                             │
                                  ▼                                             ▼
                        [Database Layer] ◄──────── (State Context) ─────── [FSM Context]
                     (aiosqlite / Transactions)
```

---

## 📐 مدیریت وضعیت کاربر (FSM)

مدیریت جریان‌های پیچیده چندمرحله‌ای به کمک کلاس‌های وضعیت اختصاصی:
```python
class TelemetryFilterState(StatesGroup):
    waiting_for_sensor_id = State()
    waiting_for_threshold = State()
    confirmation = State()
```
این ساختار ایزوله‌سازی کامل سشن‌های کاربران را تضمین می‌کند و مانع از تداخل ورودی‌های چند کاربر همزمان در تعامل با دیتابیس می‌گردد.

---

## 💻 پشته فناوری

- **فریم‌ورک اصلی:** `aiogram 3.x` (Python Asynchronous Framework)
- **پایگاه داده:** `aiosqlite` (سازگار با حلقه رویدادهای Asyncio)
- **اعتبارسنجی داده:** `Pydantic v2`
- **تولید نمودارها:** `matplotlib` جهت رسم در لحظه ترندهای تله‌متری و ارسال تصویری در تلگرام

---

## 📂 ساختار فایل‌ها

```
03-telegram-data-bot/
├── bot.py             # نقطه ورود ربات و پیکربندی Dispatcher
├── handlers/          # روترها و هندلرهای دستورات و دکمه‌های شیشه‌ای
├── middlewares/       # میدلورهای محدودسازی نرخ و لاگ‌گیری
├── database.py        # کوئری‌های ناهمگام پایگاه داده SQLite
├── requirements.txt   # بسته‌های مورد نیاز
├── README.md          # مستندات انگلیسی
└── README_FA.md       # مستندات جامع فارسی
```

---

## ⚙️ راه‌اندازی و پیکربندی

۱. ایجاد متغیرهای محیطی در فایل `.env`:
```env
BOT_TOKEN=your_telegram_bot_token_here
ADMIN_ID=123456789
DATABASE_PATH=telemetry.db
```

۲. نصب وابستگی‌ها و اجرای ربات:
```bash
pip install -r requirements.txt
python bot.py
```

---

## 📄 مجوز
این پروژه تحت مجوز [MIT](https://opensource.org/licenses/MIT) منتشر شده است.

<br />

<div align="center">
  <a href="#readme-top"><strong>بازگشت به ابتدای صفحه (Back to Top) ↑</strong></a>
</div>
