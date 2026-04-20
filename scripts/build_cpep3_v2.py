#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build cpep-config-v2.csv from manually structured C-PEP-3 data.
Data sourced from OCR of C-PEP-3测试手册&得分结果图.pdf

C-PEP-3 items have two scoring systems:
- 发展 (Development): P=通过(2), E=萌芽(1), F=不通过(0)
- 病理学 (Pathology): A=恰当(2), M=轻微(1), S=严重(0)

Some items have BOTH dev and path sub-scores, which become separate rows.
"""
import csv
import json

# Load items from JSON data file
with open("data/C-PEP/cpep3-items.json", "r", encoding="utf-8") as f:
    items = json.load(f)

# CSV header matching pep3-config-v2.csv format
HEADER = [
    "排序", "一级分类", "二级分类", "评估项目", "操作描述", "所需材料",
    "适用年龄", "是否必答",
    "评分_a_分值", "评分_a_标签", "评分_a_说明",
    "评分_b_分值", "评分_b_标签", "评分_b_说明",
    "评分_c_分值", "评分_c_标签", "评分_c_说明",
    "评分_d_分值", "评分_d_标签", "评分_d_说明",
    "评分_e_分值", "评分_e_标签", "评分_e_说明",
]

OUTPUT = "data/cpep-config-v2.csv"

rows = []
seq = 0
for item in items:
    seq += 1
    cat1 = item["cat1"]
    cat2 = item["cat2"]
    name = item["name"]
    desc = item.get("desc", "")
    materials = item.get("materials", "")
    age = item.get("age", "")

    if cat1 == "发展":
        # P/E/F -> 2/1/0, stored as a=0/不通过, b=1/萌芽, c=2/通过
        row = {
            "排序": str(seq),
            "一级分类": "发展",
            "二级分类": cat2,
            "评估项目": name,
            "操作描述": desc,
            "所需材料": materials,
            "适用年龄": age,
            "是否必答": "是",
            "评分_a_分值": "0", "评分_a_标签": "不通过",
            "评分_a_说明": item.get("f", ""),
            "评分_b_分值": "1", "评分_b_标签": "萌芽",
            "评分_b_说明": item.get("e", ""),
            "评分_c_分值": "2", "评分_c_标签": "通过",
            "评分_c_说明": item.get("p", ""),
            "评分_d_分值": "", "评分_d_标签": "", "评分_d_说明": "",
            "评分_e_分值": "", "评分_e_标签": "", "评分_e_说明": "",
        }
    else:
        # A/M/S -> 2/1/0, stored as a=0/严重, b=1/轻微, c=2/恰当
        row = {
            "排序": str(seq),
            "一级分类": "病理学",
            "二级分类": cat2,
            "评估项目": name,
            "操作描述": desc,
            "所需材料": materials,
            "适用年龄": age,
            "是否必答": "是",
            "评分_a_分值": "0", "评分_a_标签": "严重",
            "评分_a_说明": item.get("s", ""),
            "评分_b_分值": "1", "评分_b_标签": "轻微",
            "评分_b_说明": item.get("m", ""),
            "评分_c_分值": "2", "评分_c_标签": "恰当",
            "评分_c_说明": item.get("a", ""),
            "评分_d_分值": "", "评分_d_标签": "", "评分_d_说明": "",
            "评分_e_分值": "", "评分_e_标签": "", "评分_e_说明": "",
        }
    rows.append(row)

with open(OUTPUT, "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=HEADER, quoting=csv.QUOTE_ALL)
    writer.writeheader()
    writer.writerows(rows)

print(f"Generated {OUTPUT}")
print(f"Total rows: {len(rows)}")

# Stats
dev_count = sum(1 for r in rows if r["一级分类"] == "发展")
path_count = sum(1 for r in rows if r["一级分类"] == "病理学")
print(f"  发展: {dev_count}")
print(f"  病理学: {path_count}")

cat2s = set()
for r in rows:
    cat2s.add(f"{r['一级分类']} > {r['二级分类']}")
print(f"  二级分类:")
for c in sorted(cat2s):
    print(f"    {c}")
