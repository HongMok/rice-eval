#!/usr/bin/env python3
"""
Parse C-PEP-3 OCR text to generate cpep-config-v2.csv.

The PDF is the PEP-3 Chinese version test manual. The OCR text has items numbered
1A, 1B, 1C, 2, 3A, 3B, 4, 5A, 5B, ... up to 97.

Each item has:
- Item number and name
- Materials
- Procedure (操作描述)
- Domain: 发展(development) or 病理学(pathology) with subcategory
- Scoring: P/E/F (Pass/Emerging/Fail) for 发展, A/M/S (Appropriate/Mild/Severe) for 病理学

We match these to pep3-config-v2.csv rows by sequence order, then enrich
the CSV with extracted 操作描述 and 评分说明.

Output format: same 23-column structure as pep3-config-v2.csv
"""

import csv
import re
import sys

OCR_FILE = "data/C-PEP/cpep3-test-manual.txt"
PEP3_CSV = "data/pep3-config-v2.csv"
OUTPUT = "data/cpep-config-v2.csv"

V2_HEADER = [
    "排序", "一级分类", "二级分类", "评估项目", "操作描述", "所需材料",
    "适用年龄", "是否必答",
    "评分_a_分值", "评分_a_标签", "评分_a_说明",
    "评分_b_分值", "评分_b_标签", "评分_b_说明",
    "评分_c_分值", "评分_c_标签", "评分_c_说明",
    "评分_d_分值", "评分_d_标签", "评分_d_说明",
    "评分_e_分值", "评分_e_标签", "评分_e_说明",
]


def load_pep3_csv():
    rows = []
    with open(PEP3_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(dict(row))
    return rows


def extract_scoring_from_block(block_text, score_type):
    """
    Extract scoring descriptions from a text block.
    score_type: 'PEF' for development items, 'AMS' for pathology items
    
    Returns dict with keys like 'P', 'E', 'F' or 'A', 'M', 'S'
    """
    result = {}
    
    if score_type == 'PEF':
        labels = ['P', 'E', 'F']
    else:
        labels = ['A', 'M', 'S']
    
    for i, label in enumerate(labels):
        # Find "P:" or "P：" or "P," or "P、" patterns
        # The OCR sometimes produces "P:" "E:" "F:" or "A:" "M:" "S:"
        pattern = re.compile(
            rf'(?:^|\n)\s*{label}\s*[:：,，]\s*(.+?)(?=\n\s*(?:{"|".join(labels[i+1:])})\s*[:：,，]|\Z)',
            re.DOTALL
        )
        match = pattern.search(block_text)
        if match:
            desc = match.group(1).strip()
            # Clean up: remove line breaks, extra spaces
            desc = re.sub(r'\s+', ' ', desc)
            # Trim to reasonable length
            if len(desc) > 200:
                desc = desc[:200] + '...'
            result[label] = desc
    
    return result


def parse_ocr_items(ocr_text):
    """
    Parse OCR text into a list of items with whatever data we can extract.
    Returns list of dicts with keys: number, name, materials, procedure, 
    domain_type, domain_sub, scoring
    """
    items = []
    
    # Remove page separators but keep page numbers for reference
    text = re.sub(r'={10,}\n=== PAGE \d+ ===\n={10,}', '\n---PAGE_BREAK---\n', ocr_text)
    
    # Split into rough item blocks
    # Items start with patterns like:
    # "* 1 A:" or "1B:" or "2:" or "*7:" or "49C:" or "°5 2:" etc.
    # The OCR is messy so we need flexible matching
    
    # Find all scoring blocks (P/E/F or A/M/S) as they're the most reliable markers
    # We'll work backwards from scoring to find item boundaries
    
    # For now, let's just extract P/E/F and A/M/S descriptions per page
    # and try to match them to CSV items by order
    
    pages = ocr_text.split('=== PAGE ')
    
    scoring_blocks = []
    
    for page in pages:
        # Find all P: ... E: ... F: ... blocks
        pef_matches = re.finditer(
            r'P[:：]\s*(.+?)(?:\n\s*E[:：,，])\s*(.+?)(?:\n\s*F[:：,，i])\s*(.+?)(?=\n\s*(?:\d|[*°]|---PAGE|$|病理|发展|\(\d\)|[A-Z]{2,}))',
            page, re.DOTALL
        )
        for m in pef_matches:
            p_desc = re.sub(r'\s+', ' ', m.group(1).strip())[:200]
            e_desc = re.sub(r'\s+', ' ', m.group(2).strip())[:200]
            f_desc = re.sub(r'\s+', ' ', m.group(3).strip())[:200]
            scoring_blocks.append({
                'type': 'PEF',
                'P': p_desc,
                'E': e_desc,
                'F': f_desc,
            })
        
        # Find all A: ... M: ... S: ... blocks
        ams_matches = re.finditer(
            r'A[:：]\s*(.+?)(?:\n\s*M[:：,，])\s*(.+?)(?:\n\s*S[:：,，])\s*(.+?)(?=\n\s*(?:\d|[*°]|---PAGE|$|病理|发展|\(\d\)|[A-Z]{2,}))',
            page, re.DOTALL
        )
        for m in ams_matches:
            a_desc = re.sub(r'\s+', ' ', m.group(1).strip())[:200]
            m_desc = re.sub(r'\s+', ' ', m.group(2).strip())[:200]
            s_desc = re.sub(r'\s+', ' ', m.group(3).strip())[:200]
            scoring_blocks.append({
                'type': 'AMS',
                'A': a_desc,
                'M': m_desc,
                'S': s_desc,
            })
    
    return scoring_blocks


def main():
    print("Loading PEP-3 CSV as base...")
    pep3_rows = load_pep3_csv()
    print(f"  {len(pep3_rows)} items")
    
    print("Loading OCR text...")
    with open(OCR_FILE, "r", encoding="utf-8") as f:
        ocr_text = f.read()
    print(f"  {len(ocr_text)} chars")
    
    print("Parsing OCR scoring blocks...")
    scoring_blocks = parse_ocr_items(ocr_text)
    print(f"  Found {len(scoring_blocks)} scoring blocks")
    for i, sb in enumerate(scoring_blocks[:5]):
        t = sb['type']
        if t == 'PEF':
            print(f"    [{i}] PEF: P={sb['P'][:50]}...")
        else:
            print(f"    [{i}] AMS: A={sb['A'][:50]}...")
    
    # Now match scoring blocks to CSV rows
    # The CSV has 210 items. The PDF has items numbered 1-97 with sub-items.
    # Each sub-item may have 1 or 2 scoring blocks (发展 and/or 病理学).
    # The CSV rows are in the same order as the PDF items.
    
    # Strategy: iterate through CSV rows and scoring blocks together
    # - 发展 items use PEF scoring -> match to PEF blocks
    # - 行为 items use AMS scoring -> match to AMS blocks
    
    # Build the mapping based on item type
    pef_idx = 0
    ams_idx = 0
    pef_blocks = [sb for sb in scoring_blocks if sb['type'] == 'PEF']
    ams_blocks = [sb for sb in scoring_blocks if sb['type'] == 'AMS']
    
    print(f"\n  PEF blocks: {len(pef_blocks)}")
    print(f"  AMS blocks: {len(ams_blocks)}")
    
    # Count expected PEF and AMS items in CSV
    dev_count = sum(1 for r in pep3_rows if r['评分_a_标签'] in ('不通过', '不能做到'))
    beh_count = sum(1 for r in pep3_rows if r['评分_a_标签'] == '严重')
    print(f"  CSV 发展 items (不通过/不能做到): {dev_count}")
    print(f"  CSV 行为 items (严重): {beh_count}")
    
    # Enrich CSV rows with OCR scoring descriptions
    pef_i = 0
    ams_i = 0
    enriched = 0
    
    for row in pep3_rows:
        a_label = row.get('评分_a_标签', '')
        
        if a_label in ('不通过', '不能做到'):
            # Development item -> PEF scoring
            if pef_i < len(pef_blocks):
                sb = pef_blocks[pef_i]
                # Map: a=不通过(F), b=萌芽/部分做到(E), c=通过/能做到(P)
                row['评分_a_说明'] = sb.get('F', '')  # 不通过 = F
                row['评分_b_说明'] = sb.get('E', '')  # 萌芽 = E
                row['评分_c_说明'] = sb.get('P', '')  # 通过 = P
                enriched += 1
                pef_i += 1
        elif a_label == '严重':
            # Behavior/pathology item -> AMS scoring
            if ams_i < len(ams_blocks):
                sb = ams_blocks[ams_i]
                # Map: a=严重(S), b=轻微(M), c=恰当(A)
                row['评分_a_说明'] = sb.get('S', '')  # 严重 = S
                row['评分_b_说明'] = sb.get('M', '')  # 轻微 = M
                row['评分_c_说明'] = sb.get('A', '')  # 恰当 = A
                enriched += 1
                ams_i += 1
    
    print(f"\n  Enriched {enriched}/{len(pep3_rows)} items with scoring descriptions")
    print(f"  Used {pef_i}/{len(pef_blocks)} PEF blocks, {ams_i}/{len(ams_blocks)} AMS blocks")
    
    # Write output
    with open(OUTPUT, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=V2_HEADER, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        for row in pep3_rows:
            out = {}
            for h in V2_HEADER:
                out[h] = row.get(h, "")
            writer.writerow(out)
    
    print(f"\nGenerated {OUTPUT} with {len(pep3_rows)} rows")
    
    # Show some examples
    print("\nSample enriched items:")
    for i, row in enumerate(pep3_rows[:10]):
        a_desc = row.get('评分_a_说明', '')[:40]
        c_desc = row.get('评分_c_说明', '')[:40]
        print(f"  {row['排序']}. {row['评估项目'][:20]} | a说明={a_desc} | c说明={c_desc}")


if __name__ == "__main__":
    main()
