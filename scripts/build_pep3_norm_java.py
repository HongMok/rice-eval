#!/usr/bin/env python3
"""
从 config/pep3/ 下的 CSV 常模表生成 Java 文件。
CSV 文件命名格式: norm-table-{附表号}-age-{起始年龄}-{结束年龄}.csv
生成到: config/pep3/java/Pep3NormData{起始月龄}to{结束月龄}.java

用法: python scripts/build_pep3_norm_java.py
"""

import csv
import os
import re
import sys
from pathlib import Path

# 副测验代码列表（CSV 列顺序）
SUBTESTS = ["CVP", "EL", "RL", "FM", "GM", "VMI", "AE", "SR", "CMB", "CVB", "PB", "PSC", "AB"]

# 附表号 → 月龄范围映射
TABLE_AGE_MAP = {
    "1.1":  (24, 29,  "2岁0个月至2岁5个月",  "24-29月龄"),
    "1.2":  (30, 36,  "2岁6个月至3岁0个月",  "30-36月龄"),
    "1.3":  (36, 41,  "3岁0个月至3岁5个月",  "36-41月龄"),
    "1.4":  (42, 48,  "3岁6个月至4岁0个月",  "42-48月龄"),
    "1.5":  (48, 53,  "4岁0个月至4岁5个月",  "48-53月龄"),
    "1.6":  (54, 60,  "4岁6个月至5岁0个月",  "54-60月龄"),
    "1.7":  (60, 65,  "5岁0个月至5岁5个月",  "60-65月龄"),
    "1.8":  (66, 72,  "5岁6个月至6岁0个月",  "66-72月龄"),
    "1.9":  (72, 77,  "6岁0个月至6岁5个月",  "72-77月龄"),
    "1.10": (78, 84,  "6岁6个月至7岁0个月",  "78-84月龄"),
    "1.11": (84, 89,  "7岁0个月至7岁5个月",  "84-89月龄"),
}

# 年龄字符串 → 月龄
def age_str_to_months(s):
    """将 '2y0m' 格式转为月龄"""
    m = re.match(r'(\d+)y(\d+)m', s)
    if m:
        return int(m.group(1)) * 12 + int(m.group(2))
    return None


def parse_csv(csv_path):
    """
    解析 CSV 文件，返回 {subtest_code: [(raw, std, pct), ...]} 字典。
    跳过 SEM 行和空数据行。
    """
    data = {st: [] for st in SUBTESTS}

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)  # 跳过表头

        for row in reader:
            if not row or row[0].strip().upper() == 'SEM':
                continue

            raw_score = row[0].strip().strip('"')
            if not raw_score.isdigit():
                continue
            raw = int(raw_score)

            # 每个副测验占 2 列（标准分、百分比），从第 1 列开始
            for i, st in enumerate(SUBTESTS):
                col_std = 1 + i * 2
                col_pct = 2 + i * 2

                if col_std >= len(row) or col_pct >= len(row):
                    continue

                std_val = row[col_std].strip().strip('"')
                pct_val = row[col_pct].strip().strip('"')

                if not std_val or not pct_val:
                    continue

                # 标准分可能是 "<2" 这种，跳过非数字
                try:
                    std_int = int(std_val)
                except ValueError:
                    continue

                data[st].append((raw, std_int, pct_val))

    return data


def generate_java(table_num, age_from, age_to, age_desc_cn, age_desc_month, data):
    """生成 Java 文件内容"""
    class_name = f"Pep3NormData{age_from}to{age_to}"

    lines = []
    lines.append("package com.dmhxm.teaching.application.evaluate.norm;")
    lines.append("")
    lines.append("import java.util.Arrays;")
    lines.append("import java.util.HashMap;")
    lines.append("import java.util.List;")
    lines.append("import java.util.Map;")
    lines.append("")
    lines.append("/**")
    lines.append(f" * PEP-3 常模数据：{age_desc_cn}（{age_desc_month}）")
    lines.append(f" * 附表 {table_num}")
    lines.append(" *")
    lines.append(" * @author kiro")
    lines.append(" * @date 2026/4/23")
    lines.append(" */")
    lines.append(f"class {class_name} {{")
    lines.append("")
    lines.append("    static Pep3NormTable build() {")
    lines.append("        Map<String, List<Pep3NormEntry>> norms = new HashMap<>();")

    for st in SUBTESTS:
        if data[st]:
            lines.append(f'        norms.put("{st}", {st.lower()}());')

    lines.append("")
    lines.append(f"        return new Pep3NormTable({age_from}, {age_to}, norms);")
    lines.append("    }")
    lines.append("")
    lines.append("    /** 辅助方法：快速构建 entry */")
    lines.append("    private static Pep3NormEntry e(int raw, int std, String pct) {")
    lines.append("        return new Pep3NormEntry(raw, std, pct);")
    lines.append("    }")

    for st in SUBTESTS:
        entries = data[st]
        if not entries:
            continue

        lines.append("")
        lines.append(f"    // rawScore, standardScore, percentileRank")
        lines.append(f"    private static List<Pep3NormEntry> {st.lower()}() {{")
        lines.append("        return Arrays.asList(")

        # 每行 4 个 entry
        entry_strs = []
        for raw, std, pct in entries:
            entry_strs.append(f'e({raw},{std},"{pct}")')

        # 分行，每行 4 个
        for i in range(0, len(entry_strs), 4):
            chunk = entry_strs[i:i+4]
            line = "            " + ", ".join(chunk)
            if i + 4 < len(entry_strs):
                line += ","
            lines.append(line)

        lines.append("        );")
        lines.append("    }")

    lines.append("}")
    lines.append("")

    return "\n".join(lines)


def find_table_num_from_filename(filename):
    """从文件名提取附表号"""
    m = re.search(r'norm-table-(\d+\.\d+)', filename)
    if m:
        return m.group(1)
    return None


def main():
    csv_dir = Path("config/pep3")
    java_dir = Path("config/pep3/java")
    java_dir.mkdir(parents=True, exist_ok=True)

    csv_files = sorted(csv_dir.glob("norm-table-*.csv"))

    if not csv_files:
        print("未找到 CSV 常模表文件")
        sys.exit(1)

    generated = []

    for csv_file in csv_files:
        table_num = find_table_num_from_filename(csv_file.name)
        if not table_num or table_num not in TABLE_AGE_MAP:
            print(f"跳过未知附表: {csv_file.name}")
            continue

        age_from, age_to, age_desc_cn, age_desc_month = TABLE_AGE_MAP[table_num]

        print(f"处理附表 {table_num}: {csv_file.name} → Pep3NormData{age_from}to{age_to}.java")

        data = parse_csv(str(csv_file))

        # 统计
        for st in SUBTESTS:
            count = len(data[st])
            if count > 0:
                print(f"  {st}: {count} 条")

        java_content = generate_java(table_num, age_from, age_to, age_desc_cn, age_desc_month, data)

        java_path = java_dir / f"Pep3NormData{age_from}to{age_to}.java"
        with open(java_path, 'w', encoding='utf-8') as f:
            f.write(java_content)

        generated.append(java_path.name)
        print(f"  ✅ 已生成: {java_path}")

    print(f"\n共生成 {len(generated)} 个 Java 文件")
    for name in generated:
        print(f"  - {name}")


if __name__ == "__main__":
    main()
