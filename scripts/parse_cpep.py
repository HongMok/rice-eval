#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解析 C-PEP（残联版孤独症儿童发展评估表）使用手册，提取全部 493 个题目，生成 CSV。

源文件: data/PEP-3/C-PEP测试材料/cpep-usage-manual.txt
输出:   data/PEP-3/cpep-full-items.csv

策略：将所有 \\x07 (BEL) 字符替换为换行符，统一用换行符分隔的方式解析。
"""

import re
import csv
import os

INPUT_FILE = os.path.join("data", "PEP-3", "C-PEP测试材料", "cpep-usage-manual.txt")
OUTPUT_FILE = os.path.join("data", "PEP-3", "cpep-full-items.csv")

DOMAINS = [
    ("感知觉", 55, "PEF"),
    ("粗大动作", 72, "PEF"),
    ("精细动作", 66, "PEF"),
    ("语言与沟通", 79, "PEF"),
    ("认知", 55, "PEF"),
    ("社会交往", 47, "PEF"),
    ("生活自理", 67, "PEF"),
    ("情绪与行为", 52, "AMS"),
]

DOMAIN_HEADERS = [
    r"一、孤独症儿童感知觉评估表",
    r"二、孤独症儿童粗大动作评估表",
    r"三、孤独症儿童精细动作评估表",
    r"四、孤独症儿童语言与沟通评估表",
    r"五、孤独症儿童认知评估表",
    r"六、孤独症儿童社会交往评估表",
    r"七、孤独症儿童自理评估表",
    r"八、孤独症儿童情绪与行为评估表",
]


def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def find_domain_sections(text):
    positions = []
    for header in DOMAIN_HEADERS:
        m = re.search(header, text)
        if not m:
            raise ValueError(f"找不到领域标题: {header}")
        positions.append(m.start())

    domain_texts = []
    for i in range(len(positions)):
        start = positions[i]
        if i + 1 < len(positions):
            end = positions[i + 1]
        else:
            end_m = re.search(r'\n\s*备注[：:]*\s*\n[★▲]', text[start:])
            if end_m:
                end = start + end_m.start()
            else:
                end_m = re.search(r'\n附录\n', text[start:])
                end = start + end_m.start() if end_m else len(text)
        domain_texts.append(text[start:end])

    return domain_texts


def skip_header(text):
    """Skip domain header, return content start position"""
    m = re.search(r'参考\s*\n年龄\s*\n', text)
    if m:
        return m.end()
    m = re.search(r'年龄\s*\n', text)
    if m:
        return m.end()
    return 0


def clean_field(text):
    if not text:
        return ''
    text = re.sub(r'[\x07]', ' ', text)
    text = re.sub(r'\n+', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def normalize_content(text):
    """Replace \\x07 with \\n and clean up"""
    text = text.replace('\x07', '\n')
    # Collapse multiple blank lines
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text


def parse_scoring(text, score_type):
    """Extract scoring descriptions from text"""
    scores = {}
    if score_type == "PEF":
        labels = [('P', '高'), ('E', '中'), ('F', '低')]
    else:
        labels = [('A', '高'), ('M', '中'), ('S', '低')]

    for mark, level in labels:
        scores[level] = ''

    if score_type == "PEF":
        p_m = re.search(r'P[-—:](.+?)(?=E[-—:])', text, re.DOTALL)
        e_m = re.search(r'E[-—:](.+?)(?=F[-—:])', text, re.DOTALL)
        f_m = re.search(r'F[-—:](.+)', text, re.DOTALL)
        if p_m:
            scores['高'] = clean_field(p_m.group(1))
        if e_m:
            scores['中'] = clean_field(e_m.group(1))
        if f_m:
            val = f_m.group(1)
            # Remove trailing age
            val = re.sub(r'\s*\d+[-–]\d+月?\s*$', '', val)
            scores['低'] = clean_field(val)
    else:
        a_m = re.search(r'A[-—](.+?)(?=M[-—])', text, re.DOTALL)
        m_m = re.search(r'M[-—](.+?)(?=S[-—])', text, re.DOTALL)
        s_m = re.search(r'S[-—](.+)', text, re.DOTALL)
        if a_m:
            scores['高'] = clean_field(a_m.group(1))
        if m_m:
            scores['中'] = clean_field(m_m.group(1))
        if s_m:
            scores['低'] = clean_field(s_m.group(1))

    return scores


def make_item(num, domain_name, score_type):
    item = {
        '排序': str(num),
        '分组': domain_name,
        '领域': '',
        '评估项目': '',
        '操作描述': '',
        '所需材料': '',
        '适用年龄': '',
        '是否必答': '是',
    }
    if score_type == "PEF":
        item.update({
            '评分分值_高_标签': '通过',
            '评分分值_高_说明': '',
            '评分分值_中_标签': '中间反应',
            '评分分值_中_说明': '',
            '评分分值_低_标签': '不通过',
            '评分分值_低_说明': '',
        })
    else:
        item.update({
            '评分分值_高_标签': '没有',
            '评分分值_高_说明': '',
            '评分分值_中_标签': '轻度',
            '评分分值_中_说明': '',
            '评分分值_低_标签': '严重',
            '评分分值_低_说明': '',
        })
    return item


def find_item_boundaries(lines, expected_count):
    """Find line indices where each item starts (item number line)"""
    # Build list of (line_index, item_number, markers) for all matching lines
    candidates = []
    for li, line in enumerate(lines):
        stripped = line.strip()
        m = re.match(r'^([★▲●]*)(\d{1,2})\s*$', stripped)
        if m:
            candidates.append((li, int(m.group(2)), m.group(1)))

    # Greedily match sequential item numbers 1, 2, 3, ...
    matched = []
    expected_num = 1
    for li, num, markers in candidates:
        if num == expected_num:
            matched.append((li, num, markers))
            expected_num += 1
            if expected_num > expected_count:
                break

    return matched


def parse_item_lines(item_lines, item, score_type):
    """Parse the content lines of a single item (between item number and next item)"""
    if not item_lines:
        return

    # Find scoring start
    scoring_start = -1
    score_marker = 'P' if score_type == "PEF" else 'A'
    for i, line in enumerate(item_lines):
        if re.match(rf'^{score_marker}[-—:]', line.strip()):
            scoring_start = i
            break

    # Extract scoring and age
    if scoring_start >= 0:
        scoring_text = '\n'.join(item_lines[scoring_start:])
        scores = parse_scoring(scoring_text, score_type)
        item['评分分值_高_说明'] = scores['高']
        item['评分分值_中_说明'] = scores['中']
        item['评分分值_低_说明'] = scores['低']

        # Find age (usually last non-empty line)
        for line in reversed(item_lines[scoring_start:]):
            stripped = line.strip()
            age_m = re.match(r'^(\d+[-–]\d+)(?:月)?\s*$', stripped)
            if age_m:
                item['适用年龄'] = age_m.group(1).replace('–', '-') + '月'
                break

        pre_lines = [l.strip() for l in item_lines[:scoring_start] if l.strip()]
    else:
        pre_lines = [l.strip() for l in item_lines if l.strip()]

    if not pre_lines:
        return

    # Parse pre-scoring lines: subdomain, project, material, method
    parse_header_fields(pre_lines, item)


def parse_header_fields(lines, item):
    """Parse subdomain, project name, material, and method from pre-scoring lines.

    The lines between item number and scoring follow this order:
    [领域大类] [子领域] 评估项目 [材料] 操作描述

    Strategy: find description start, then the line immediately before description
    is the material. Everything before that is domain/subdomain/project.
    """
    if not lines:
        return

    # Find method/description start
    desc_start = find_description_start(lines)

    if desc_start < len(lines):
        item['操作描述'] = clean_field('\n'.join(lines[desc_start:]))

    header_lines = lines[:desc_start]

    if not header_lines:
        return

    # Filter out empty lines
    non_empty = [l for l in header_lines if l.strip()]

    if not non_empty:
        return

    # The last non-empty header line is the material (if it exists and is recognizable)
    # The line before that is the project name
    # Everything before that is domain/subdomain

    # Check if last line is material
    last_line = non_empty[-1].strip()
    is_mat = is_material_line(last_line)

    if is_mat:
        if '观察项目' in last_line:
            item['所需材料'] = '观察项目'
        elif last_line == '无':
            item['所需材料'] = '无'
        else:
            item['所需材料'] = clean_field(last_line)
        pre_material = non_empty[:-1]
    elif len(non_empty) >= 4:
        # If we have 4+ non-empty lines and the last one isn't recognized as material,
        # it's still likely the material (the table always has this column).
        # Unless it looks like a domain/project name.
        if len(last_line) < 50 and not any(kw in last_line for kw in ['能力', '概念', '技巧', '礼仪']):
            item['所需材料'] = clean_field(last_line)
            pre_material = non_empty[:-1]
        else:
            pre_material = non_empty
    else:
        pre_material = non_empty

    # Parse domain and project from pre_material lines
    if len(pre_material) == 0:
        pass
    elif len(pre_material) == 1:
        item['评估项目'] = clean_field(pre_material[0])
    elif len(pre_material) == 2:
        item['领域'] = clean_field(pre_material[0])
        item['评估项目'] = clean_field(pre_material[1])
    elif len(pre_material) == 3:
        item['领域'] = clean_field(pre_material[0] + pre_material[1])
        item['评估项目'] = clean_field(pre_material[2])
    else:
        # 4+ lines: combine all but last as domain, last as project
        item['领域'] = clean_field(' '.join(pre_material[:-1]))
        item['评估项目'] = clean_field(pre_material[-1])


def find_description_start(lines):
    """Find the line index where the method/description starts"""
    desc_keywords = [
        '测试员', '测试人员', '评估员', '在距离', '在儿童面前', '让儿童',
        '对儿童说', '在日常', '询问家长', '设计情境', '将所有',
        '儿童舒适', '儿童面对', '蒙住', '把图片', '翻开图片',
        '从五张', '把碗', '把玩具', '将其中', '将两', '将玩具',
        '把所有', '要求儿童', '用勺子', '用汤匙', '把纸笔',
        '在儿童目睹', '将积木', '把红绿', '把黄蓝', '吸引儿童',
        '在没有动作', '照顾者去抱', '儿童不熟悉', '观察儿童',
        '分别让', '拿出少量', '观察问题', '儿童在刚进入',
        '儿童对测试', '儿童是否', '当测试员', '儿童单独',
        '饭后让', '把碗递给', '儿童坐在', '儿童站立',
        '将所有物件', '在没有', '测试员手持', '将一件',
        '把图片放', '将图片', '将其中的', '将两张',
        '在儿童面前摆放', '将积木放', '把所有积木',
        '将全部', '将拼图', '将已完成', '将模板',
        '将动物模板', '将3只', '将已完成的',
        '观察儿童日常', '儿童坐在地面', '儿童坐在楼梯',
        '让儿童双膝', '测试员坐在', '测试员示范',
        '测试员将', '测试员在', '测试员拿', '测试员面对',
        '测试员让', '测试员吸引', '测试员先',
        '照顾者', '用勺子将', '儿童舒适的',
        '在测试时', '在测试中',
    ]

    for i, line in enumerate(lines):
        if i == 0:
            continue  # First line is usually subdomain/project
        stripped = line.strip()
        for kw in desc_keywords:
            if stripped.startswith(kw):
                return i
            # Also check if keyword appears early in a long line
            if len(stripped) > 20 and kw in stripped[:40]:
                return i
        # Long lines (>30 chars) that aren't material are likely descriptions
        if i >= 2 and len(stripped) > 35:
            return i

    return len(lines)


def find_material_line(header_lines):
    """Find the line index containing material info"""
    for i, line in enumerate(header_lines):
        stripped = line.strip()
        if is_material_line(stripped):
            return i
    return -1


def is_material_line(text):
    """Check if a line is a material/tool description"""
    text = text.strip()
    if not text:
        return False

    # Explicit material markers
    if text == '观察项目' or text.startswith('观察项目'):
        return True
    if text == '无':
        return True

    # Quantity keywords
    mat_kws = [
        '1支', '1只', '1个', '1套', '1本', '1块', '1张', '1盒',
        '1份', '1条', '1根', '1把', '1卷', '1瓶', '各1', '各2',
        '各3', '各4', '各5', '若干', '秒表', '地垫', '2套', '2只',
        '2个', '3块', '4块', '5块', '6块', '7块', '8块', '12块',
        '10张', '15副', '各一', '一只', '一个', '一套', '一份',
        '一条', '一根', '一块', '一张', '一本', '一盒',
    ]
    for kw in mat_kws:
        if kw in text:
            return True

    # Common material names (without quantity words)
    material_names = [
        '玩具', '积木', '气球', '拼图', '拼板', '拼块', '图片', '卡片',
        '铅笔', '画笔', '彩色笔', '记号笔', '蜡笔',
        '剪刀', '胶棒', '橡皮', '直尺', '纸', '白纸', '格子纸',
        '镜子', '万花筒', '手电筒', '摇铃', '音叉', '响板', '哨子',
        '喇叭', '小鼓', '录音', '布娃娃',
        '糖果', '饼干', '蜂蜜', '食物', '饮料', '水果',
        '奶瓶', '汤匙', '勺子', '杯子', '碗', '筷子',
        '毛巾', '手帕', '衣服', '鞋', '袜', '纽扣',
        '绳子', '细绳', '珠子', '橡皮泥',
        '触觉块', '海绵', '木块', '铁块',
        '文件袋', '塑料袋', '容器', '盒子', '罐',
        '同上',
    ]
    for name in material_names:
        if name in text and len(text) < 60:
            return True

    return False


def parse_domain(domain_text, domain_name, expected_count, score_type):
    """Parse all items from a domain section"""
    content_start = skip_header(domain_text)
    content = domain_text[content_start:]

    # Remove trailing notes
    备注_m = re.search(r'\n\s*备注[：:]*', content)
    if 备注_m:
        content = content[:备注_m.start()]

    # Normalize: replace \x07 with \n
    content = normalize_content(content)

    lines = content.split('\n')

    # Find item boundaries
    boundaries = find_item_boundaries(lines, expected_count)

    if len(boundaries) != expected_count:
        print(f"    找到 {len(boundaries)}/{expected_count} 个题号")

    items = []
    current_domain = ''

    for idx, (start_li, num, markers) in enumerate(boundaries):
        if idx + 1 < len(boundaries):
            end_li = boundaries[idx + 1][0]
        else:
            end_li = len(lines)

        item_lines = lines[start_li + 1:end_li]
        item = make_item(num, domain_name, score_type)

        parse_item_lines(item_lines, item, score_type)

        # Track and fill domain
        if item['领域']:
            current_domain = item['领域']
        elif current_domain:
            item['领域'] = current_domain

        items.append(item)

    return items


def write_csv(items, output_path):
    headers = [
        '排序', '分组', '领域', '评估项目', '操作描述', '所需材料',
        '适用年龄', '是否必答',
        '评分分值_高_标签', '评分分值_高_说明',
        '评分分值_中_标签', '评分分值_中_说明',
        '评分分值_低_标签', '评分分值_低_说明',
    ]
    with open(output_path, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        for item in items:
            writer.writerow(item)


def main():
    print(f"读取源文件: {INPUT_FILE}")
    text = read_file(INPUT_FILE)
    print(f"文件总行数: {len(text.splitlines())}")

    domain_texts = find_domain_sections(text)

    all_items = []
    total = 0

    for i, (domain_name, expected_count, score_type) in enumerate(DOMAINS):
        print(f"\n解析领域: {domain_name} (期望 {expected_count} 题)")

        items = parse_domain(domain_texts[i], domain_name, expected_count, score_type)

        print(f"  实际提取: {len(items)} 题")
        total += len(items)
        all_items.extend(items)

    print(f"\n总计: {total} 题")

    write_csv(all_items, OUTPUT_FILE)
    print(f"\nCSV 已生成: {OUTPUT_FILE}")

    print("\n=== 验证 ===")
    for domain_name, expected_count, _ in DOMAINS:
        actual = sum(1 for item in all_items if item['分组'] == domain_name)
        status = "✓" if actual == expected_count else "✗"
        print(f"  {status} {domain_name}: {actual}/{expected_count}")

    target = sum(d[1] for d in DOMAINS)
    status = "✓" if total == target else "✗"
    print(f"  {status} 总计: {total}/{target}")


if __name__ == '__main__':
    main()
