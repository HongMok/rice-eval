#!/usr/bin/env python3
"""
Generate cpep-config-v2.csv from cpep-config.csv.

Changes from v1 to v2:
1. Add columns for up to 5 scoring levels (d, e) to match pep3-config-v2.csv format
2. Fix scoring values: 中间反应/轻度 should have a value (not empty)
3. Reorder scoring from low to high (0=worst → 2=best) to match pep3-v2 convention
4. All fields quoted (QUOTE_ALL), UTF-8 encoding
"""
import csv

INPUT = "data/cpep-config.csv"
OUTPUT = "data/cpep-config-v2.csv"

# v2 header matches pep3-config-v2.csv structure
V2_HEADER = [
    "排序", "一级分类", "二级分类", "评估项目", "操作描述", "所需材料",
    "适用年龄", "是否必答",
    "评分_a_分值", "评分_a_标签", "评分_a_说明",
    "评分_b_分值", "评分_b_标签", "评分_b_说明",
    "评分_c_分值", "评分_c_标签", "评分_c_说明",
    "评分_d_分值", "评分_d_标签", "评分_d_说明",
    "评分_e_分值", "评分_e_标签", "评分_e_说明",
]

rows_out = []

with open(INPUT, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        cat1 = row["一级分类"]
        
        # v1 scoring: a=通过(1)/没有(空), b=中间反应(空)/轻度(空), c=不通过(0)/严重(空)
        a_label = row["评分_a_标签"]
        b_label = row["评分_b_标签"]
        c_label = row["评分_c_标签"]
        a_desc = row["评分_a_说明"]
        b_desc = row["评分_b_说明"]
        c_desc = row["评分_c_说明"]
        
        # v2 convention: reorder from lowest score to highest score
        # For 发展类 (通过/中间反应/不通过): 0=不通过, 1=中间反应, 2=通过 (but v1 has 1/empty/0)
        # For 情绪与行为 (没有/轻度/严重): 0=严重, 1=轻度, 2=没有
        
        if cat1 == "情绪与行为":
            # v1: a=没有(空分值), b=轻度(空分值), c=严重(空分值)
            # v2: a=0/严重, b=1/轻微, c=2/没有 (low to high, matching pep3-v2 behavior subtest pattern)
            out_row = {
                "排序": row["排序"],
                "一级分类": row["一级分类"],
                "二级分类": row["二级分类"],
                "评估项目": row["评估项目"],
                "操作描述": row["操作描述"],
                "所需材料": row["所需材料"],
                "适用年龄": row["适用年龄"],
                "是否必答": row["是否必答"],
                "评分_a_分值": "0",
                "评分_a_标签": "严重",
                "评分_a_说明": c_desc,  # 严重的说明
                "评分_b_分值": "1",
                "评分_b_标签": "轻微",
                "评分_b_说明": b_desc,  # 轻度的说明
                "评分_c_分值": "2",
                "评分_c_标签": "没有",
                "评分_c_说明": a_desc,  # 没有的说明
                "评分_d_分值": "",
                "评分_d_标签": "",
                "评分_d_说明": "",
                "评分_e_分值": "",
                "评分_e_标签": "",
                "评分_e_说明": "",
            }
        else:
            # 发展类: v1: a=通过(1), b=中间反应(空), c=不通过(0)
            # v2: a=0/不通过, b=1/中间反应, c=2/通过 (low to high, matching pep3-v2 dev subtest pattern)
            out_row = {
                "排序": row["排序"],
                "一级分类": row["一级分类"],
                "二级分类": row["二级分类"],
                "评估项目": row["评估项目"],
                "操作描述": row["操作描述"],
                "所需材料": row["所需材料"],
                "适用年龄": row["适用年龄"],
                "是否必答": row["是否必答"],
                "评分_a_分值": "0",
                "评分_a_标签": "不通过",
                "评分_a_说明": c_desc,  # 不通过的说明
                "评分_b_分值": "1",
                "评分_b_标签": "中间反应",
                "评分_b_说明": b_desc,  # 中间反应的说明
                "评分_c_分值": "2",
                "评分_c_标签": "通过",
                "评分_c_说明": a_desc,  # 通过的说明
                "评分_d_分值": "",
                "评分_d_标签": "",
                "评分_d_说明": "",
                "评分_e_分值": "",
                "评分_e_标签": "",
                "评分_e_说明": "",
            }
        
        rows_out.append(out_row)

# Write v2 CSV
with open(OUTPUT, "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=V2_HEADER, quoting=csv.QUOTE_ALL)
    writer.writeheader()
    writer.writerows(rows_out)

print(f"Generated {OUTPUT} with {len(rows_out)} rows")
print(f"Header columns: {len(V2_HEADER)}")

# Verify
with open(OUTPUT, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    patterns = set()
    for row in reader:
        labels = []
        for key in ["评分_a_标签", "评分_b_标签", "评分_c_标签"]:
            val = row.get(key, "")
            if val:
                labels.append(f"{row[key.replace('标签','分值')]}/{val}")
        patterns.add(" | ".join(labels))
    print("\nScoring patterns in v2:")
    for p in sorted(patterns):
        print(f"  {p}")
