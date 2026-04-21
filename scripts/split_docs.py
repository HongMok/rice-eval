#!/usr/bin/env python3
"""Split large docs into per-page md files based on ## 界面N headings."""
import re, os

SPLITS = [
    {
        "src": "docs/assessment-admin.md",
        "dir": "docs/assessment-admin",
        "mapping": {
            "admin-assessment-list": ["界面1", "界面2", "界面3"],
            "admin-assessment-edit": ["界面4", "界面5", "界面6", "界面7"],
            "admin-assessment-import": ["界面8"],
        },
        "header_section": "系统界面跳转关系",
    },
    {
        "src": "docs/assessment-app.md",
        "dir": "docs/assessment-app",
        "mapping": {
            "assessment-list": ["界面1", "界面8"],
            "assessment-intro": ["界面2"],
            "assessment-answer": ["界面3"],
            "assessment-result": ["界面4"],
            "assessment-result-pep3": ["界面5"],
            "assessment-result-cpep": ["界面6"],
            "assessment-result-vbmapp": ["界面7"],
            "assessment-result-parent": ["界面9"],
        },
        "header_section": "系统界面跳转关系",
    },
]

def split_by_h2(content):
    """Split markdown by ## headings, return dict of heading_prefix -> content."""
    sections = {}
    current_key = "_header"
    current_lines = []
    
    for line in content.split('\n'):
        m = re.match(r'^## (界面\d+)', line)
        if m:
            sections[current_key] = '\n'.join(current_lines)
            current_key = m.group(1)
            current_lines = [line]
        else:
            current_lines.append(line)
    sections[current_key] = '\n'.join(current_lines)
    return sections

def main():
    for spec in SPLITS:
        src = spec["src"]
        if not os.path.exists(src):
            print(f"Skip {src}: not found")
            continue
        
        with open(src, "r", encoding="utf-8") as f:
            content = f.read()
        
        sections = split_by_h2(content)
        os.makedirs(spec["dir"], exist_ok=True)
        
        # Get header (title + jump relations)
        header = sections.get("_header", "")
        header_section = ""
        if spec["header_section"] in header:
            idx = header.find("## " + spec["header_section"])
            if idx >= 0:
                header_section = header[idx:]
        
        for filename, section_keys in spec["mapping"].items():
            parts = []
            for key in section_keys:
                if key in sections:
                    parts.append(sections[key].strip())
            
            if parts:
                out = '\n\n---\n\n'.join(parts)
            else:
                out = f"# {filename}\n\n> 待补充"
            
            # Prepend header section to first file only? No, each file self-contained
            outpath = os.path.join(spec["dir"], f"{filename}.md")
            with open(outpath, "w", encoding="utf-8") as f:
                f.write(out + "\n")
            print(f"  {outpath}: {len(out)} chars, {len(parts)} sections")

if __name__ == "__main__":
    main()
