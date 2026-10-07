import sys
import os
import tempfile
from datetime import datetime
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from database import BotDatabase
from bot import parse_natural_query
from customer_rfm_segmentation import CustomerRfmSegmenter
from invoice_generator import ProformaInvoiceGenerator


def test_bot_database_operations():
    db = BotDatabase(db_path=":memory:")
    # Search items
    results = db.search_items("لپ‌تاپ")
    assert len(results) >= 1
    for r in results:
        assert "لپ‌تاپ" in r["title"] or "لپ‌تاپ" in r["category"]

    # Price filtered search
    affordable = db.search_items("لپ‌تاپ", max_price=40_000_000)
    for item in affordable:
        assert item["price"] <= 40_000_000

    # Alerts subscription
    alert_id = db.subscribe_price_alert(user_id=12345, target_product="ایسوس", target_price=40_000_000)
    assert alert_id > 0
    matched_users = db.check_alerts("لپ‌تاپ ایسوس Vivobook", 38_500_000)
    assert 12345 in matched_users

    # Stats
    stats = db.get_summary_stats()
    assert stats["total_items"] > 0
    assert stats["avg_price"] > 0


def test_parse_natural_query():
    kw, budget = parse_natural_query("گوشی زیر 20 میلیون")
    assert "گوشی" in kw
    assert budget == 20_000_000

    kw2, budget2 = parse_natural_query("مانیتور گیمینگ")
    assert budget2 is None
    assert "مانیتور گیمینگ" in kw2


def test_customer_rfm_segmentation():
    segmenter = CustomerRfmSegmenter(reference_date=datetime(2026, 10, 5))
    orders = [
        {"customer_id": "cust_1", "date": "2026-10-02", "amount_toman": 50_000_000},
        {"customer_id": "cust_1", "date": "2026-09-25", "amount_toman": 60_000_000},
        {"customer_id": "cust_1", "date": "2026-09-10", "amount_toman": 40_000_000},
        {"customer_id": "cust_1", "date": "2026-09-01", "amount_toman": 20_000_000},
        {"customer_id": "cust_2", "date": "2026-05-01", "amount_toman": 2_000_000},
    ]
    res = segmenter.segment_customers(orders)
    assert res["total_customers"] == 2
    assert res["total_revenue_toman"] == 172_000_000
    assert len(res["top_valuable_customers"]) >= 1
    assert res["top_valuable_customers"][0]["customer_id"] == "cust_1"


def test_proforma_invoice_pdf_generation():
    generator = ProformaInvoiceGenerator(seller_name="Test Engineering Store")
    items = [
        {"name": "Industrial Sensor Modbus", "qty": 2, "unit_price": 5_000_000},
        {"name": "Power Supply 24V 5A", "qty": 1, "unit_price": 2_500_000},
    ]
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        out_path = tmp.name

    try:
        pdf_path = generator.generate_invoice_pdf(
            invoice_number="INV-2026-001",
            customer_name="شرکت توسعه صنعتی",
            customer_phone="09121112233",
            items=items,
            output_filepath=out_path
        )
        assert os.path.exists(pdf_path)
        assert os.path.getsize(pdf_path) > 1000
    finally:
        if os.path.exists(out_path):
            os.remove(out_path)
