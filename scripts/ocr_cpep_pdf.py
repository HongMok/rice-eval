#!/usr/bin/env python3
"""
OCR extract C-PEP-3 test manual PDF to text.
The PDF is a scanned document (image-based), so we use tesseract OCR.
"""
import pdfplumber
import pytesseract
from PIL import Image
import sys
import os

PDF_PATH = "data/C-PEP/C-PEP-3测试手册&得分结果图.pdf"
OUTPUT_PATH = "data/C-PEP/cpep3-test-manual.txt"

# Pages with assessment items (1-indexed): 3-47 based on scan
START_PAGE = 3  # 0-indexed: 2
END_PAGE = 48   # 0-indexed: 47

print(f"Opening {PDF_PATH}...")
pdf = pdfplumber.open(PDF_PATH)
print(f"Total pages: {len(pdf.pages)}")

all_text = []

for i in range(START_PAGE - 1, min(END_PAGE, len(pdf.pages))):
    page = pdf.pages[i]
    print(f"  OCR page {i+1}...", end=" ", flush=True)
    
    # Convert to high-res image for better OCR
    img = page.to_image(resolution=300)
    pil_img = img.annotated
    
    # OCR with Chinese + English
    text = pytesseract.image_to_string(
        pil_img, 
        lang='chi_sim+eng',
        config='--psm 6'
    )
    
    all_text.append(f"\n{'='*80}")
    all_text.append(f"=== PAGE {i+1} ===")
    all_text.append(f"{'='*80}\n")
    all_text.append(text)
    
    lines = len(text.strip().split('\n'))
    print(f"{lines} lines")

pdf.close()

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(all_text))

print(f"\nDone! Saved to {OUTPUT_PATH}")
print(f"Total text length: {sum(len(t) for t in all_text)} chars")
