<a id="readme-top"></a>

<div align="center">

[![English Documentation](https://img.shields.io/badge/Documentation-English-blue.svg?style=for-the-badge)](README.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/Python-3.10%2B-3776AB.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Framework: aiogram](https://img.shields.io/badge/Framework-aiogram_3.x-2CA5E0.svg?style=for-the-badge&logo=telegram&logoColor=white)](https://aiogram.dev/)
[![Database: SQLite](https://img.shields.io/badge/Database-SQLite3_Async-003B57.svg?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)

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
