#!/usr/bin/env python3
"""Extract text and tables from C-PEP PDF."""
import pdfplumber
import sys

pdf_path = "data/C-PEP/C-PEP-3测试手册&得分结果图.pdf"
output_path = "data/C-PEP/cpep3-test-manual.txt"

with pdfplumber.open(pdf_path) as pdf:
    all_text = []
    for i, page in enumerate(pdf.pages):
        all_text.append(f"\n{'='*80}")
        all_text.append(f"=== PAGE {i+1} ===")
        all_text.append(f"{'='*80}\n")
        
        # Try to extract tables first
        tables = page.extract_tables()
        if tables:
            for t_idx, table in enumerate(tables):
                all_text.append(f"--- TABLE {t_idx+1} ---")
                for row in table:
                    cleaned = [str(cell).strip() if cell else "" for cell in row]
                    all_text.append(" | ".join(cleaned))
                all_text.append("")
        
        # Also extract full text
        text = page.extract_text()
        if text:
            all_text.append("--- TEXT ---")
            all_text.append(text)

with open(output_path, "w", encoding="utf-8") as f:
    f.write("\n".join(all_text))

print(f"Extracted {len(pdf.pages)} pages to {output_path}")
