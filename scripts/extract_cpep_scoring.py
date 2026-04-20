#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extract scoring descriptions from OCR text and cpep3-items.json,
then generate data/cpep-config-v2.csv.

Strategy:
1. Read pep3-config-v2.csv as the base structure (210 rows, correct ordering)
2. Use cpep3-items.json for items it contains (clean, pre-extracted)
3. For remaining items, manually map scoring descriptions from OCR analysis
4. Generate cpep-config-v2.csv with all scoring descriptions filled in
"""

import csv
import json
import os
import re

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_CSV = os.path.join(BASE_DIR, 'data', 'pep3-config-v2.csv')
ITEMS_JSON = os.path.join(BASE_DIR, 'data', 'C-PEP', 'cpep3-items.json')
OUTPUT_CSV = os.path.join(BASE_DIR, 'data', 'cpep-config-v2.csv')

# Read base CSV
rows = []
with open(BASE_CSV, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        rows.append(list(row))

print(f"Read {len(rows)} rows from base CSV")

# Column indices
COL_A_DESC = 10   # 评分_a_说明
COL_B_DESC = 13   # 评分_b_说明
COL_C_DESC = 16   # 评分_c_说明

# Try to read cpep3-items.json
json_items = []
try:
    with open(ITEMS_JSON, 'r', encoding='utf-8') as f:
        content = f.read()
        # Fix potential JSON issues - the file might have trailing content
        # Try to parse as-is first
        try:
            json_items = json.loads(content)
        except json.JSONDecodeError:
            # Try to fix common issues
            # Remove trailing commas before ] or }
            content = re.sub(r',\s*([}\]])', r'\1', content)
            json_items = json.loads(content)
    print(f"Read {len(json_items)} items from cpep3-items.json")
except Exception as e:
    print(f"Error reading cpep3-items.json: {e}")
    print("Will use manual mapping only")

# Build a lookup from json items by their id
json_lookup = {}
for item in json_items:
    json_lookup[item['id']] = item

print(f"JSON lookup has {len(json_lookup)} entries")
print(f"JSON item IDs: {list(json_lookup.keys())}")
