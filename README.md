# 🤖 Polyglot Telegram Data Service & Bot (Python + TypeScript)

A hybrid bot architecture combining a **TypeScript edge webhook receiver** with an **asynchronous Python analytics & search core**.

## 🌟 Polyglot Architecture
- **TypeScript Webhook Gateway (`typescript_webhook_gateway/`):** Ultra-fast HTTP handler for zero-cold-start webhook processing.
- **Python Bot Core (`bot.py`):** Business logic, catalog search, and spreadsheet analytics.

## 🎯 Real-World Applications & Cross-Industry Impact
### ⚙️ E-Commerce & Retail
- Instant inventory lookup, budget filtering, and price-drop alerts.
### 🌐 Cross-Industry & Software
- Cloud event dispatching for DevOps alarms and server health monitoring.

## 🚀 Execution
```bash
# TypeScript Gateway:
cd typescript_webhook_gateway && node src/server.ts

# Python Core:
pip install -r requirements.txt && python bot.py
```

## 👨‍💻 Author
**Ardavan Ghal-Eh** | Sharif University of Technology
