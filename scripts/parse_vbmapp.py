#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Parse VB-MAPP domain classification and generate milestones CSV."""

import csv
import re
import sys

# Domain name mappings
DOMAIN_MAP = {
    '提要求': ('Mand(提要求)', 'Mand'),
    '命名': ('Tact(命名)', 'Tact'),
    '听者反应': ('Listener(听者反应)', 'Listener'),
    '视觉感知和样本配对': ('VP/MTS(视觉配对)', 'VP-MTS'),
    '独立游戏': ('Play(游戏)', 'Play'),
    '社会行为和社会游戏': ('Social(社交)', 'Social'),
    '动作模仿': ('Imitation(模仿)', 'Imitation'),
    '对功能、特性和类别的听者反应（LRFFC）': ('LRFFC(听者功能)', 'LRFFC'),
    '对功能、特性和类别的听者反应': ('LRFFC(听者功能)', 'LRFFC'),
    '对话': ('Intraverbal(对话)', 'Intraverbal'),
    '教室常规和集体技能': ('Group(集体技能)', 'Group'),
    '语言结构': ('Linguistics(语言结构)', 'Linguistics'),
    '阅读': ('Reading(阅读)', 'Reading'),
    '书写': ('Writing(书写)', 'Writing'),
    '算术': ('Math(算术)', 'Math'),
}

# Stage mappings
STAGE_MAP = {
    '1': ('Level 1 (0-18月)', '0-18月'),
    '2': ('Level 2 (18-30月)', '18-30月'),
    '3': ('Level 3 (30-48月)', '30-48月'),
}


def clean_description(desc):
    """Clean up a description: join lines, remove trailing (T)/(E)/(O) markers and punctuation."""
    # Join multi-line text into single line
    desc = re.sub(r'\s*\n\s*', '', desc)
    desc = desc.strip()
    # Remove trailing (T), (E), (O) markers (both full-width and half-width parens)
    desc = re.sub(r'\s*[（(][TEO][）)]\s*$', '', desc)
    # Remove trailing punctuation
    desc = desc.rstrip('。．')
    return desc.strip()


def parse_vbmapp(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        text = f.read()

    rows = []
    sort_order = 0

    # Split by domain-stage headers
    # Pattern: "领域名——第 X 阶段" or "领域名——第X阶段"
    section_pattern = re.compile(
        r'^(.+?)——第\s*(\d)\s*阶段',
        re.MULTILINE
    )

    sections = list(section_pattern.finditer(text))

    for i, section_match in enumerate(sections):
        domain_raw = section_match.group(1).strip()
        stage_num = section_match.group(2)

        # Get section text
        start = section_match.end()
        end = sections[i + 1].start() if i + 1 < len(sections) else len(text)
        section_text = text[start:end]

        # Look up domain
        domain_name, domain_abbrev = lookup_domain(domain_raw)

        # Look up stage
        stage_label, age_range = STAGE_MAP.get(stage_num, (f'Level {stage_num}', ''))

        # Parse all items (sub-steps and milestones) in this section
        # Pattern matches: number-letter (e.g., 1-a, 1-M, 8- M, 12-b)
        item_pattern = re.compile(
            r'^(\d+)-\s*([a-zA-Z])\s*\n(.*?)(?=^\d+-\s*[a-zA-Z]\s*$|\Z)',
            re.MULTILINE | re.DOTALL
        )

        # Collect all items grouped by milestone number
        # For each milestone number X, collect sub-steps (X-a, X-b, ...) and milestone (X-M)
        items_by_num = {}  # {num: {'substeps': [(letter, desc), ...], 'milestone_desc': str}}

        for item_match in item_pattern.finditer(section_text):
            num = int(item_match.group(1))
            letter = item_match.group(2).strip()
            raw_desc = item_match.group(3).strip()

            if num not in items_by_num:
                items_by_num[num] = {'substeps': [], 'milestone_desc': ''}

            desc = clean_description(raw_desc)

            if letter.upper() == 'M':
                items_by_num[num]['milestone_desc'] = desc
            else:
                items_by_num[num]['substeps'].append((f'{num}-{letter}', desc))

        # Generate rows for each milestone in order
        for num in sorted(items_by_num.keys()):
            data = items_by_num[num]
            milestone_desc = data['milestone_desc']
            substeps = data['substeps']

            sort_order += 1
            item_name = f'{domain_abbrev} {num}'

            # Build 0.5 score description from sub-steps
            if substeps:
                substep_parts = []
                for label, desc in substeps:
                    if desc:  # skip empty descriptions
                        substep_parts.append(f'({label}) {desc}')
                half_score_desc = '; '.join(substep_parts) if substep_parts else '部分达到里程碑描述的标准'
            else:
                half_score_desc = '部分达到里程碑描述的标准'

            # Handle empty milestone descriptions (English grammar items)
            if not milestone_desc:
                row = {
                    '排序': sort_order,
                    '分组': stage_label,
                    '领域': domain_name,
                    '评估项目': item_name,
                    '操作描述': '(此里程碑为英语语法特有项目，中文版不适用)',
                    '所需材料': '',
                    '适用年龄': age_range,
                    '是否必答': '否',
                    '评分说明_1_达标': '完全达到里程碑描述的标准',
                    '评分说明_0.5_部分达标': half_score_desc if substeps else '部分达到里程碑描述的标准',
                    '评分说明_0_未达标': '以上行为均未观察到',
                }
                rows.append(row)
                continue

            row = {
                '排序': sort_order,
                '分组': stage_label,
                '领域': domain_name,
                '评估项目': item_name,
                '操作描述': milestone_desc,
                '所需材料': '',
                '适用年龄': age_range,
                '是否必答': '是',
                '评分说明_1_达标': milestone_desc,
                '评分说明_0.5_部分达标': half_score_desc,
                '评分说明_0_未达标': '以上行为均未观察到',
            }
            rows.append(row)

    # Write CSV
    fieldnames = [
        '排序', '分组', '领域', '评估项目', '操作描述', '所需材料',
        '适用年龄', '是否必答', '评分说明_1_达标', '评分说明_0.5_部分达标', '评分说明_0_未达标',
    ]

    with open(output_path, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Generated {len(rows)} rows in {output_path}")
    return rows


def lookup_domain(raw):
    """Look up domain name and abbreviation."""
    raw = raw.strip()

    # Try exact match first
    if raw in DOMAIN_MAP:
        return DOMAIN_MAP[raw]

    # Try partial match
    for key, val in DOMAIN_MAP.items():
        if key in raw or raw in key:
            return val

    # Fallback
    print(f"WARNING: Unknown domain: '{raw}'", file=sys.stderr)
    return (raw, raw)


if __name__ == '__main__':
    parse_vbmapp('data/VB/vbmapp-domain-classification.txt', 'data/VB/vbmapp-full-milestones.csv')
