#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Parse PEP-3 original items and generate CSV."""

import csv
import re
import sys

# Colon pattern: matches both ： and ；
CP = r'[：:；;]'

def parse_pep3(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # Find where supplement section starts
    supplement_start = text.find('附：补充测试步骤')
    if supplement_start == -1:
        supplement_start = text.find('补充测试步骤')
    if supplement_start == -1:
        supplement_start = len(text)
    
    main_text = text[:supplement_start]
    
    # Pattern to match item headers
    # Handles: "1 A任务：", "1A任务：", "2任务：", "*8A任务：", "l 1 B任务：", "7 1行为：", etc.
    # Note: some items use ， (Chinese comma) instead of ： (Chinese colon)
    item_pattern = re.compile(
        r'(?:^|\n)\s*\*?'
        r'([0-9l][0-9 l]*[0-9]?)\s*'
        r'([A-E]?)\s*'
        r'(任务|行为)[：:；;，,]\s*'
        r'(.+?)(?=\n)',
        re.MULTILINE
    )
    
    items = []
    matches = list(item_pattern.finditer(main_text))
    
    for i, match in enumerate(matches):
        start = match.start()
        end = matches[i+1].start() if i+1 < len(matches) else supplement_start
        
        block = main_text[start:end].strip()
        
        raw_num = match.group(1).replace(' ', '').replace('l', '1')
        letter = match.group(2).strip()
        task_type = match.group(3)
        task_name = match.group(4).strip()
        
        item_id = raw_num + (letter if letter else '')
        
        items.append({
            'raw_num': raw_num,
            'letter': letter,
            'task_type': task_type,
            'task_name': task_name,
            'block': block,
            'item_id': item_id,
        })
    
    # Parse each item
    rows = []
    sort_order = 0
    
    for item in items:
        block = item['block']
        
        # Extract 材料
        mat_pat = re.compile(r'材料' + CP + r'\s*(.+?)(?=\n\s*(?:实施|观察|功能|病理|评分))', re.DOTALL)
        material_match = mat_pat.search(block)
        material = ''
        if material_match:
            material = material_match.group(1).strip()
            material = re.sub(r'\s+', '', material)
        
        # Extract 实施/观察
        op_pat = re.compile(r'(?:实施|观察)' + CP + r'\s*(.+?)(?=\n\s*(?:功能|病理|评分))', re.DOTALL)
        operation_match = op_pat.search(block)
        operation = ''
        if operation_match:
            operation = operation_match.group(1).strip()
            operation = re.sub(r'\n\s*', '', operation)
        
        # Extract domains
        domains = extract_domains(block)
        
        if not domains:
            print(f"WARNING: No domain found for item {item['item_id']}: {item['task_name']}", file=sys.stderr)
            domains = [('未知', False)]
        
        # Extract scoring sections
        scoring_map = extract_scoring(block, domains)
        
        sort_order += 1
        
        for di, (domain, is_behavioral) in enumerate(domains):
            # Determine group
            if is_behavioral:
                group = '行为表现'
            else:
                group = '功能发展'
            
            # Get scoring
            s2, s1, s0 = scoring_map.get(di, ('', '', ''))
            
            row = {
                '排序': sort_order,
                '分组': group,
                '领域': domain,
                '评估项目': item['task_name'],
                '操作描述': operation,
                '所需材料': material,
                '适用年龄': '',
                '是否必答': '是',
                '评分说明_2_通过': s2,
                '评分说明_1_萌芽': s1,
                '评分说明_0_不通过': s0,
            }
            rows.append(row)
    
    # Write CSV
    fieldnames = ['排序', '分组', '领域', '评估项目', '操作描述', '所需材料', '适用年龄', '是否必答', '评分说明_2_通过', '评分说明_1_萌芽', '评分说明_0_不通过']
    
    with open(output_path, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    
    print(f"Generated {len(rows)} rows in {output_path}")
    return rows


def extract_domains(block):
    """Extract domains from a block. Returns list of (domain_name, is_behavioral) tuples."""
    domains = []
    
    # Patterns for domain lines (match both ： and ；)
    # 1. "功能领域：XXX" or "功能领域；XXX"
    # 2. "病理学领域：XXX" or "病理领域：XXX"
    # 3. "功能及病理学领域：此项任务在两个领域评分：(1)XXX及(2)YYY"
    # 4. "功能领域：此项任务从两个功能方面评分：(1)XXX及(2)YYY"
    
    # First check for combined func+patho line
    combined_pat = re.compile(
        r'功能及病理(?:学)?领域' + CP + r'\s*此项(?:任务)?在两个领域评分' + CP + r'\s*'
        r'[（(]1[）)]\s*(.+?)\s*及\s*[（(]?\s*2\s*[）)]?\s*(.+?)(?:\n|$)'
    )
    m = combined_pat.search(block)
    if m:
        d1 = clean_domain(m.group(1))
        d2 = clean_domain(m.group(2))
        domains.append(classify_domain(d1))
        domains.append(classify_domain(d2))
        return domains
    
    # Check for "功能领域：此项任务从两个功能方面评分" or similar
    dual_func_pat = re.compile(
        r'功能领域' + CP + r'\s*此项任务(?:从|正|在)两个功能方面评分' + CP + r'\s*'
        r'[（(]1[）)]\s*(.+?)\s*及\s*[（(]\s*2\s*[）)]\s*(.+?)(?:\n|$)'
    )
    m = dual_func_pat.search(block)
    if m:
        d1 = clean_domain(m.group(1))
        d2 = clean_domain(m.group(2))
        domains.append(classify_domain(d1))
        domains.append(classify_domain(d2))
        return domains
    
    # Check for dual domain in "功能及病理学领域" with different format
    dual_mixed_pat = re.compile(
        r'功能及病理(?:学)?领域' + CP + r'\s*此项(?:任务)?在两个(?:领域|功能)评分' + CP + r'\s*'
        r'[（(]1[）)]\s*(.+?)\s*及\s*[（(]?\s*2\s*[）)]?\s*(.+?)(?:\n|$)'
    )
    m = dual_mixed_pat.search(block)
    if m:
        d1 = clean_domain(m.group(1))
        d2 = clean_domain(m.group(2))
        domains.append(classify_domain(d1))
        domains.append(classify_domain(d2))
        return domains
    
    # Single function domain
    func_pat = re.compile(r'功能领域' + CP + r'\s*(.+?)(?:\n|$)')
    m = func_pat.search(block)
    if m:
        d = m.group(1).strip()
        # Check if it contains dual domain info
        # Matches: "此项任务从两个功能方面评分", "这项任务在两个功能方面评分", etc.
        dual_m = re.search(r'(?:此项|这项)任务(?:从|正|在)两个功能(?:方面)?评分' + CP + r'\s*[（(]1[）)]\s*(.+?)\s*及\s*[（(]\s*2\s*[）)]\s*(.+?)(?:。|$)', d)
        if dual_m:
            d1 = clean_domain(dual_m.group(1))
            d2 = clean_domain(dual_m.group(2))
            domains.append(classify_domain(d1))
            domains.append(classify_domain(d2))
            return domains
        
        d = clean_domain(d)
        domains.append(classify_domain(d))
    
    # Single pathology domain
    patho_pat = re.compile(r'病理(?:学)?领域' + CP + r'\s*(.+?)(?:\n|$)')
    m = patho_pat.search(block)
    if m:
        d = m.group(1).strip()
        d = clean_domain(d)
        domains.append(classify_domain(d))
    
    return domains


def clean_domain(d):
    """Clean up a domain string."""
    d = d.strip()
    # Remove trailing punctuation
    d = d.rstrip('。．,，;；')
    # Remove leading/trailing whitespace
    d = d.strip()
    return d


def classify_domain(domain):
    """Classify domain and return (normalized_name, is_behavioral)."""
    behavioral_keywords = ['病理', '感觉', '感情', '游戏', '语言', '人际关系', '合作行为']
    
    is_behavioral = any(kw in domain for kw in behavioral_keywords)
    
    # Normalize domain name
    normalized = normalize_domain(domain)
    
    return (normalized, is_behavioral)


def normalize_domain(domain):
    """Normalize domain names to standard form."""
    domain = domain.strip().rstrip('。．,，;；')
    
    # Direct mappings
    mappings = [
        ('精细动作', '精细动作'),
        ('模仿(动作)', '模仿(动作)'),
        ('模仿（动作）', '模仿(动作)'),
        ('模仿(口语)', '模仿(口语)'),
        ('模仿（口语）', '模仿(口语)'),
        ('模仿(U语)', '模仿(口语)'),
        ('知觉(视觉)', '知觉(视觉)'),
        ('知觉（视觉）', '知觉(视觉)'),
        ('知觉<听觉)', '知觉(听觉)'),
        ('知觉(听觉)', '知觉(听觉)'),
        ('知觉领域(听觉)', '知觉(听觉)'),
        ('手眼协调', '手眼协调'),
        ('认知表现', '认知表现'),
        ('口语认知', '口语认知'),
        ('粗大动作', '粗大动作'),
        ('感觉反应', '感觉'),
        ('感觉', '感觉'),
        ('感情', '感情'),
        ('游戏及对物的兴趣', '游戏及对物的兴趣'),
        ('语言', '语言'),
        ('病理学领域(感觉)', '感觉'),
        ('病理学(感觉)', '感觉'),
        ('病理(感觉)', '感觉'),
    ]
    
    for key, val in mappings:
        if domain == key:
            return val
    
    # Partial matching
    if '人际关系' in domain or '合作行为' in domain:
        return '人际关系'
    if '游戏' in domain and '对物' in domain:
        return '游戏及对物的兴趣'
    if '知觉' in domain and '听觉' in domain:
        return '知觉(听觉)'
    if '知觉' in domain and '视觉' in domain:
        return '知觉(视觉)'
    if '知觉' in domain:
        return '知觉(视觉)'
    if '病理' in domain and '感觉' in domain:
        return '感觉'
    if '病理' in domain and '感情' in domain:
        return '感情'
    if '感觉' in domain:
        return '感觉'
    
    return domain


def extract_scoring(block, domains):
    """Extract scoring for each domain. Returns dict of {domain_index: (s2, s1, s0)}."""
    result = {}
    
    # Find all 评分 sections
    # Pattern: 评分：(N) or 评分；(N) or just 评分：
    score_sections = re.split(r'\n\s*评分' + CP, block)
    
    if len(score_sections) <= 1:
        # No scoring found - try alternate pattern where scoring is inline
        # e.g., "评分；参见图33：菱形仿画评分标准．\n通过：..."
        alt_score = re.search(r'评分' + CP + r'.*?\n((?:.*通过|.*没有)' + CP + r'.+)', block, re.DOTALL)
        if alt_score:
            score_text = alt_score.group(1)
            is_behavioral = len(domains) > 0 and domains[0][1]
            s2, s1, s0 = parse_scoring_text(score_text, is_behavioral)
            result[0] = (s2, s1, s0)
            return result
        
        return result
    
    # Process each scoring section (skip the first split which is before any 评分)
    for section in score_sections[1:]:
        section = section.strip()
        
        # Check if it starts with a domain number like "(1)" or "(2)"
        num_match = re.match(r'\s*[（(](\d)[）)]\s*', section)
        domain_idx = None
        
        if num_match:
            domain_idx = int(num_match.group(1)) - 1
            section = section[num_match.end():]
        
        # Determine if behavioral or functional scoring
        is_behavioral = '没有' in section and ('轻度' in section or '中度' in section)
        is_functional = '通过' in section and ('中间反应' in section or '通不过' in section)
        
        if not is_behavioral and not is_functional:
            # Check if there's scoring text after a reference line
            # e.g., "参见图33：菱形仿画评分标准．\n通过：..."
            remaining = section
            if '通过' in remaining:
                is_functional = True
            elif '没有' in remaining:
                is_behavioral = True
            else:
                continue
        
        s2, s1, s0 = parse_scoring_text(section, is_behavioral)
        
        if domain_idx is not None:
            result[domain_idx] = (s2, s1, s0)
        else:
            # Assign to the appropriate domain
            if len(domains) == 1:
                result[0] = (s2, s1, s0)
            else:
                # Try to match by type
                for di, (d, is_beh) in enumerate(domains):
                    if di not in result:
                        if is_behavioral and is_beh:
                            result[di] = (s2, s1, s0)
                            break
                        elif is_functional and not is_beh:
                            result[di] = (s2, s1, s0)
                            break
                else:
                    # Fallback: assign to first unassigned
                    for di in range(len(domains)):
                        if di not in result:
                            result[di] = (s2, s1, s0)
                            break
    
    return result


def parse_scoring_text(score_text, is_behavioral):
    """Parse scoring text and return (s2, s1, s0)."""
    # Flatten multiline
    score_text = re.sub(r'\n\s*', '', score_text)
    
    s2 = s1 = s0 = ''
    
    if is_behavioral:
        # 没有/轻度(or中度)/重度
        m = re.search(r'没有' + CP + r'\s*(.+?)(?=(?:轻度|中度)' + CP + r'|$)', score_text)
        if m: s2 = m.group(1).strip().rstrip('。．')
        m = re.search(r'(?:轻度|中度)' + CP + r'\s*(.+?)(?=重度' + CP + r'|$)', score_text)
        if m: s1 = m.group(1).strip().rstrip('。．')
        m = re.search(r'重度' + CP + r'\s*(.+?)$', score_text)
        if m: s0 = m.group(1).strip().rstrip('。．')
    else:
        # 通过/中间反应/通不过
        # Note: some source texts have OCR error where 通不过 is written as 通过
        # Handle by checking for 通不过 first, then 通过
        m_fail = re.search(r'通不过' + CP + r'\s*(.+?)$', score_text)
        if m_fail:
            s0 = m_fail.group(1).strip().rstrip('。．')
        
        m = re.search(r'通过' + CP + r'\s*(.+?)(?=中间反应' + CP + r'|$)', score_text)
        if m: s2 = m.group(1).strip().rstrip('。．')
        m = re.search(r'中间反应' + CP + r'\s*(.+?)(?=通不过' + CP + r'|$)', score_text)
        if m: 
            s1 = m.group(1).strip().rstrip('。．')
        else:
            # If no 通不过, check if 中间反应 is followed by another 通过 (OCR error)
            m = re.search(r'中间反应' + CP + r'\s*(.+?)(?=通过' + CP + r'|$)', score_text)
            if m: s1 = m.group(1).strip().rstrip('。．')
        
        # If 通不过 wasn't found but there's a second 通过, treat it as 通不过
        if not s0:
            # Find all 通过 matches
            pass_matches = list(re.finditer(r'通过' + CP + r'\s*', score_text))
            if len(pass_matches) >= 2:
                # The second 通过 is actually 通不过 (OCR error)
                second_start = pass_matches[1].end()
                s0 = score_text[second_start:].strip().rstrip('。．')
    
    return s2, s1, s0


if __name__ == '__main__':
    parse_pep3('data/PEP-3/pep3-original-items.txt', 'data/PEP-3/pep3-full-items.csv')
