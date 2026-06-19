#!/usr/bin/env python3
"""Normalize PDF ligature characters in all raw text chunks."""

import os, re, glob

RAW_DIR = "/home/lightdesk/MyPrompts/extracted_prompts"
LIGATURE_MAP = {
    '\ufb00': 'ff',  # ﬀ
    '\ufb01': 'fi',  # ﬁ
    '\ufb02': 'fl',  # ﬂ
    '\ufb03': 'ffi', # ﬃ
    '\ufb04': 'ffl', # ﬄ
}

for fpath in sorted(glob.glob(f"{RAW_DIR}/raw_text_*.txt")):
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    normalized = content
    for lig, repl in LIGATURE_MAP.items():
        normalized = normalized.replace(lig, repl)
    
    if normalized != content:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(normalized)
        print(f"  Normalized: {os.path.basename(fpath)}")
    else:
        print(f"  No ligatures: {os.path.basename(fpath)}")

print("Done.")
