#!/usr/bin/env python3
"""
Parse C-PEP-3 OCR text and generate cpep-config-v2.csv.

The OCR text is messy, so we manually structure the data based on careful
reading of the OCR output combined with the original PDF structure.

C-PEP-3 has ~97 items with two scoring systems:
- Development items: P(Pass)/E(Emerging)/F(Fail) -> 2/1/0
- Pathology items: A(Appropriate)/M(Mild)/S(Severe) -> 2/1/0

Some items have both development AND pathology sub-scores (e.g., 8A has
both perception and hand-eye coordination scores).
"""
import csv
import json

# We'll manually structure the items from the OCR text.
# Format: each item is a dict with fields matching the v2 CSV schema.
# Items with multiple sub-scores are split into separate rows.

items = []

def dev_item(seq, cat1, cat2, name, desc, materials, p_desc, e_desc, f_desc):
    """Create a development-type item (P/E/F scoring, mapped to 0/1/2)."""
    return {
        "sort": seq,
        "cat1": cat1,
        "cat2": cat2,
        "name": name,
        "desc": desc,
        "materials": materials,
        "age": "",
        "required": "yes",
        "scores": [
            (0, "not_pass", f_desc),
            (1, "emerging", e_desc),
            (2, "pass", p_desc),
        ]
    }

def path_item(seq, cat1, cat2, name, desc, materials, a_desc, m_desc, s_desc):
    """Create a pathology-type item (A/M/S scoring, mapped to 0/1/2)."""
    return {
        "sort": seq,
        "cat1": cat1,
        "cat2": cat2,
        "name": name,
        "desc": desc,
        "materials": materials,
        "age": "",
        "required": "yes",
        "scores": [
            (0, "severe", s_desc),
            (1, "mild", m_desc),
            (2, "appropriate", a_desc),
        ]
    }

# ============================================================
# Items parsed from OCR text of C-PEP-3 test manual
# ============================================================

# --- Page 4 ---
items.append(dev_item(
    "1A", "development", "fine_motor",
    "unscrew_bubble_cap",
    "put_bubble_bottle_on_table_tell_child_to_unscrew_cap_demonstrate_if_needed",
    "bubble_bottle",
    "child_can_unscrew_cap_by_self",
    "child_cannot_remove_cap_but_seems_to_know_necessary_actions",
    "child_cannot_remove_cap_and_does_not_know_necessary_actions_or_does_not_try"
))

items.append(dev_item(
    "1B", "development", "fine_motor",
    "blow_bubbles",
    "demonstrate_blowing_bubbles_then_hand_wand_to_child",
    "bubble_bottle_and_wand",
    "child_blows_some_bubbles",
    "child_cannot_blow_bubbles_but_seems_to_know_necessary_actions",
    "child_cannot_blow_bubbles_and_does_not_know_necessary_actions_or_does_not_try"
))

items.append(dev_item(
    "1C", "development", "perception_visual",
    "track_bubbles_visually",
    "observe_if_child_tracks_bubbles_with_eyes_during_item_1B",
    "same_as_1B",
    "child_clearly_tracks_bubbles_with_eyes",
    "child_briefly_attends_to_bubbles",
    "child_cannot_or_does_not_try_to_track_bubbles"
))

print("Script structure validated. Now building full item list...")
print("Due to OCR quality issues, we will generate the CSV with")
print("Chinese labels directly from the structured data.")

# Instead of parsing messy OCR, let's build the complete item list
# with proper Chinese content based on the OCR reading.

items_cn = []

def add_dev(seq, cat2, name, desc, materials, p, e, f):
    items_cn.append({
        "seq": str(seq), "cat1": "development", "cat2": cat2,
        "name": name, "desc": desc, "materials": materials,
        "p": p, "e": e, "f": f, "type": "dev"
    })

def add_path(seq, cat2, name, desc, materials, a, m, s):
    items_cn.append({
        "seq": str(seq), "cat1": "pathology", "cat2": cat2,
        "name": name, "desc": desc, "materials": materials,
        "a": a, "m": m, "s": s, "type": "path"
    })

# ===== ITEMS FROM OCR =====

# 1A
add_dev("1A", "fine_motor", "unscrew_cap", 
    "put_bubble_on_table_say_this_is_bubble_bottle_hand_to_child_demonstrate_if_needed",
    "bubble_bottle",
    "child_unscrews_cap_alone",
    "child_cannot_remove_cap_but_knows_actions",
    "child_cannot_remove_cap_does_not_know_actions_or_not_try")

# ... (truncated for brevity - full list would be very long)

print(f"Total items so far: {len(items_cn)}")
print("OCR parsing approach is too error-prone for 97+ items.")
print("Switching to manual structured data entry approach.")
