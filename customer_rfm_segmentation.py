"""
Customer RFM Segmentation & Lifetime Value (LTV) Clustering Module
Part of Telegram Business & Inventory Automation Suite
Author: Ardavan Ghal-Eh | Sharif University of Technology
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Any


class CustomerRfmSegmenter:
    """
    Performs Recency, Frequency, and Monetary (RFM) behavioral clustering
    for Telegram e-commerce shops to drive personalized marketing and retention.
    """

    def __init__(self, reference_date: datetime = None):
        self.reference_date = reference_date or datetime.now()

    def segment_customers(self, transactions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        transactions: list of dicts [{'customer_id': 'user_101', 'date': '2026-09-20', 'amount_toman': 38_500_000}, ...]
        """
        if not transactions:
            return {"total_customers": 0, "segments": {}}

        df = pd.DataFrame(transactions)
        df['date'] = pd.to_datetime(df['date'])

        # Aggregate per customer
        rfm = df.groupby('customer_id').agg(
            recency_days=('date', lambda d: (self.reference_date - d.max()).days),
            frequency=('date', 'count'),
            monetary=('amount_toman', 'sum')
        ).reset_index()

        # Score 1 to 5 (or quantiles)
        def score_recency(r):
            if r <= 7: return 5
            elif r <= 20: return 4
            elif r <= 45: return 3
            elif r <= 90: return 2
            else: return 1

        def score_frequency(f):
            if f >= 5: return 5
            elif f >= 3: return 4
            elif f >= 2: return 3
            elif f == 1: return 2
            else: return 1

        def score_monetary(m):
            if m >= 100_000_000: return 5
            elif m >= 50_000_000: return 4
            elif m >= 20_000_000: return 3
            elif m >= 5_000_000: return 2
            else: return 1

        rfm['R'] = rfm['recency_days'].apply(score_recency)
        rfm['F'] = rfm['frequency'].apply(score_frequency)
        rfm['M'] = rfm['monetary'].apply(score_monetary)
        rfm['RFM_Score'] = rfm['R'].astype(str) + rfm['F'].astype(str) + rfm['M'].astype(str)

        # Categorize into Actionable Marketing Segments
        def label_segment(row):
            r, f = row['R'], row['F']
            if r >= 4 and f >= 4:
                return "🌟 مشتریان طلایی و قهرمان (Champions)"
            elif r >= 3 and f >= 3:
                return "💎 وفادار و سودآور (Loyal Customers)"
            elif r >= 4 and f <= 2:
                return "🌱 خریداران جدید با پتانسیل (Recent Customers)"
            elif r <= 2 and f >= 3:
                return "⚠️ در معرض ریزش (At Risk / Needs Attention)"
            elif r <= 2 and f <= 2:
                return "💤 کم‌فعال و در خواب (Hibernating)"
            else:
                return "📌 مشتریان بالقوه (Promising)"

        rfm['Segment'] = rfm.apply(label_segment, axis=1)

        summary = rfm['Segment'].value_counts().to_dict()
        top_spenders = rfm.sort_values(by='monetary', ascending=False).head(3).to_dict(orient='records')

        return {
            "total_customers": len(rfm),
            "total_revenue_toman": int(rfm['monetary'].sum()),
            "average_customer_ltv_toman": int(rfm['monetary'].mean()),
            "segment_distribution": summary,
            "top_valuable_customers": top_spenders
        }


def run_demo_rfm():
    segmenter = CustomerRfmSegmenter(reference_date=datetime(2026, 10, 5))
    sample_orders = [
        {"customer_id": "09121112233", "date": "2026-10-02", "amount_toman": 42_000_000},
        {"customer_id": "09121112233", "date": "2026-09-15", "amount_toman": 18_500_000},
        {"customer_id": "09121112233", "date": "2026-08-10", "amount_toman": 55_000_000},
        {"customer_id": "09358889900", "date": "2026-10-04", "amount_toman": 3_500_000},
        {"customer_id": "09194445566", "date": "2026-07-20", "amount_toman": 72_000_000},
        {"customer_id": "09194445566", "date": "2026-06-15", "amount_toman": 34_000_000},
        {"customer_id": "09307771122", "date": "2026-05-10", "amount_toman": 1_200_000},
    ]

    res = segmenter.segment_customers(sample_orders)

    print("=" * 65)
    print("👥 بخش‌بندی هوشمند مشتریان بر پایه متدولوژی RFM در تلگرام:")
    print("=" * 65)
    print(f"تعداد کل مشتریان تحلیل‌شده: {res['total_customers']}")
    print(f"ارزش کل خریدهای ثبت‌شده: {res['total_revenue_toman']:,} تومان")
    print(f"میانگین ارزش طول عمر مشتری (LTV): {res['average_customer_ltv_toman']:,} تومان")
    print("توزیع بخش‌های رفتاری مشتریان:")
    for seg, cnt in res['segment_distribution'].items():
        print(f"  - {seg}: {cnt} مشتری")
    print("=" * 65)


if __name__ == "__main__":
    run_demo_rfm()
