"""
Official Pro-Forma Invoice PDF Generator Module
Part of Telegram Business Automation Bot Suite
Author: Ardavan Ghal-Eh | Sharif University of Technology
"""

import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors


class ProformaInvoiceGenerator:
    """
    Generates standard, professional commercial pro-forma invoices in PDF format.
    Suitable for sending directly to customers on Telegram or WhatsApp.
    """

    def __init__(self, seller_name: str = "بازرگانی و خدمات مهندسی آریا"):
        self.seller_name = seller_name

    def generate_invoice_pdf(
        self,
        invoice_number: str,
        customer_name: str,
        customer_phone: str,
        items: list,
        output_filepath: str = "proforma_invoice.pdf",
        vat_rate: float = 0.10
    ) -> str:
        """
        Builds a standard PDF invoice with line items, VAT calculation, and grand total.
        """
        doc = SimpleDocTemplate(
            output_filepath,
            pagesize=A4,
            rightMargin=36,
            leftMargin=36,
            topMargin=36,
            bottomMargin=36
        )

        styles = getSampleStyleSheet()
        elements = []

        title_style = ParagraphStyle(
            'InvoiceTitle',
            parent=styles['Heading1'],
            fontSize=18,
            leading=22,
            alignment=1, # Center
            textColor=colors.HexColor('#1B365D')
        )

        meta_style = ParagraphStyle(
            'MetaStyle',
            parent=styles['Normal'],
            fontSize=10,
            leading=14,
            textColor=colors.HexColor('#333333')
        )

        elements.append(Paragraph("<b>PRO-FORMA INVOICE / پیش‌فاکتور فروش کالا و خدمات</b>", title_style))
        elements.append(Spacer(1, 15))

        # Header Info Table
        today_str = datetime.now().strftime("%Y-%m-%d")
        header_data = [
            [f"Invoice No / شماره فاکتور: {invoice_number}", f"Date / تاریخ: {today_str}"],
            [f"Seller / فروشنده: {self.seller_name}", "Validity / اعتبار: 7 Days (۷ روز کاری)"],
            [f"Buyer / خریدار: {customer_name}", f"Tel / تماس: {customer_phone}"]
        ]
        header_table = Table(header_data, colWidths=[270, 250])
        header_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F4F6F9')),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
            ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,-1), 9),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('TOPPADDING', (0,0), (-1,-1), 6),
        ]))
        elements.append(header_table)
        elements.append(Spacer(1, 20))

        # Items Table
        table_data = [
            ["Row", "Item Description / شرح کالا", "Qty", "Unit Price (Toman)", "Total (Toman)"]
        ]

        subtotal = 0
        for idx, item in enumerate(items, 1):
            qty = item.get("qty", 1)
            unit_price = item.get("unit_price", 0)
            line_total = qty * unit_price
            subtotal += line_total
            table_data.append([
                str(idx),
                item.get("description", "کالا"),
                str(qty),
                f"{unit_price:,}",
                f"{line_total:,}"
            ])

        vat_amount = int(subtotal * vat_rate)
        grand_total = subtotal + vat_amount

        # Summary Rows
        table_data.append(["", "", "", "Subtotal / جمع کل اقلام:", f"{subtotal:,}"])
        table_data.append(["", "", "", f"VAT (10%) / مالیات بر ارزش افزوده:", f"{vat_amount:,}"])
        table_data.append(["", "", "", "Grand Total / مبلغ نهایی قابل پرداخت:", f"{grand_total:,} Toman"])

        items_table = Table(table_data, colWidths=[35, 235, 45, 100, 105])
        items_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1B365D')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('ALIGN', (1,1), (1,-1), 'LEFT'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,0), 9),
            ('GRID', (0,0), (-1,-4), 0.5, colors.HexColor('#CBD5E1')),
            ('LINEBELOW', (0,-4), (-1,-4), 1.5, colors.HexColor('#1B365D')),
            ('BACKGROUND', (3,-3), (-1,-1), colors.HexColor('#F8FAFC')),
            ('FONTNAME', (3,-1), (-1,-1), 'Helvetica-Bold'),
            ('TEXTCOLOR', (3,-1), (-1,-1), colors.HexColor('#0F766E')),
            ('FONTSIZE', (3,-1), (-1,-1), 10),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('TOPPADDING', (0,0), (-1,-1), 6),
        ]))
        elements.append(items_table)
        elements.append(Spacer(1, 30))

        # Footer notes
        footer_text = (
            "Payment Terms: Cash before delivery. Bank Transfer to Official IBAN.<br/>"
            "شرایط تسویه: تسویه کامل قبل از ارسال بار. لطفاً فیش واریز را در بات تلگرام آپلود فرمایید.<br/>"
            "This invoice is digitally signed and generated via Telegram Automated Data Engine."
        )
        elements.append(Paragraph(footer_text, meta_style))

        doc.build(elements)
        return output_filepath


def run_demo_invoice():
    generator = ProformaInvoiceGenerator()
    demo_items = [
        {"description": "ASUS Vivobook 15 Laptop (Core i7, 16GB)", "qty": 2, "unit_price": 38_500_000},
        {"description": "Wireless Mechanical Keyboard", "qty": 4, "unit_price": 2_800_000},
        {"description": "27-inch 165Hz IPS Monitor", "qty": 2, "unit_price": 14_200_000}
    ]
    filepath = generator.generate_invoice_pdf(
        invoice_number="INV-2026-1042",
        customer_name="شرکت توسعه فناوری پارس",
        customer_phone="09121112233",
        items=demo_items,
        output_filepath="sample_proforma_invoice.pdf"
    )
    print("=" * 65)
    print(f"📄 پیش‌فاکتور رسمی با موفقیت تولید شد: {filepath} ({os.path.getsize(filepath)} bytes)")
    print("=" * 65)


if __name__ == "__main__":
    run_demo_invoice()
