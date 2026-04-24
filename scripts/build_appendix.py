#!/usr/bin/env python3
"""
将 config 下的 iep/report/scoring 文档整理成附录，
所有原始标题降2级，确保飞书文档目录层级正确。

层级结构：
  # 附录                          (H1)
  ## 附录A：评分规则               (H2)
    #### 1. xxx                   (H4) — 原 ## 降2级
    ##### 1.1 xxx                 (H5) — 原 ### 降2级
  ## 附录B：评估报告计算规则        (H2)
    ### B.1 通用报告规则            (H3)
      #### 1. xxx                 (H4) — 原 ## 降2级
"""

import re

def read_and_demote(path):
    """Read file, remove H1 and leading blockquotes, demote headings by 2 levels."""
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read().strip()

    # Remove first H1 line
    content = re.sub(r'^#\s+[^\n]+\n', '', content, count=1).strip()

    # Remove leading > blockquote lines
    lines = content.split('\n')
    while lines and lines[0].startswith('>'):
        lines.pop(0)
    while lines and lines[0].strip() == '':
        lines.pop(0)
    content = '\n'.join(lines)

    # Demote headings by 2 levels: process from deepest to shallowest
    # to avoid double-processing
    def demote_heading(m):
        hashes = m.group(1)
        rest = m.group(2)
        return '#' * (len(hashes) + 2) + ' ' + rest

    content = re.sub(r'^(#{2,6}) (.+)$', demote_heading, content, flags=re.MULTILINE)

    return content


structure = [
    {
        'code': 'A',
        'title': '评分规则',
        'file': 'config/scoring-mode-rules.md',
    },
    {
        'code': 'B',
        'title': '评估报告计算规则',
        'children': [
            ('B.1', '通用报告规则', 'config/report-prompt-common.md'),
            ('B.2', 'PEP-3 报告规则', 'config/report-prompt-pep3.md'),
            ('B.3', 'C-PEP 报告规则', 'config/report-prompt-cpep.md'),
            ('B.4', 'VB-MAPP 报告规则', 'config/report-prompt-vbmapp.md'),
        ],
    },
    {
        'code': 'C',
        'title': 'IEP 生成规则',
        'children': [
            ('C.1', '通用 IEP 规则', 'config/iep-prompt-common.md'),
            ('C.2', 'PEP-3 IEP 规则', 'config/iep-prompt-pep3.md'),
            ('C.3', 'C-PEP IEP 规则', 'config/iep-prompt-cpep.md'),
            ('C.4', 'VB-MAPP IEP 规则', 'config/iep-prompt-vbmapp.md'),
        ],
    },
]

out = ['---\n\n# 附录\n']

for item in structure:
    code = item['code']
    title = item['title']

    if 'file' in item:
        content = read_and_demote(item['file'])
        out.append(f'---\n\n## 附录{code}：{title}\n\n{content}\n')
    elif 'children' in item:
        out.append(f'---\n\n## 附录{code}：{title}\n')
        for sub_code, sub_title, sub_path in item['children']:
            content = read_and_demote(sub_path)
            out.append(f'\n### {sub_code} {sub_title}\n\n{content}\n')

result = '\n'.join(out)

with open('docs/assessment-app-appendix.md', 'w', encoding='utf-8') as f:
    f.write(result)

print(f'Done: {len(result)} chars')

# Verify heading hierarchy
print('\nHeading hierarchy:')
for line in result.split('\n'):
    if re.match(r'^#{1,6} ', line):
        level = len(line.split(' ')[0])
        print(f'  H{level}: {line[:70]}')
