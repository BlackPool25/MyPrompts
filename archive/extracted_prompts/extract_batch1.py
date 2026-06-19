#!/usr/bin/env python3
"""Verbatim prompt extractor - extracts ALL prompts from all raw text chunk files.
Pure cut-and-paste from source text, NO generation or rewriting."""

import os, re

RAW_DIR = "/home/lightdesk/MyPrompts/extracted_prompts"
OUT_DIR = "/home/lightdesk/MyPrompts/extracted_prompts/prompts"

def read_raw(filename):
    with open(os.path.join(RAW_DIR, filename), "r") as f:
        return f.read()

def write_prompt(path, content):
    with open(path, "w") as f:
        f.write(content)

def strip_page_annotations(text):
    """Remove printed page annotations"""
    return re.sub(r"\n?Printed using ChatGPT to PDF, powered by PDFCrowd HTML to PDF API\. \d+/190\n?", "", text)

# Read all raw chunks
chunks = sorted([f for f in os.listdir(RAW_DIR) if f.startswith("raw_text_") and f.endswith(".txt")])
raw_full = ""
for c in chunks:
    raw_full += read_raw(c) + "\n"

# =======================================================================
# P001 — User: "Make this prompt better..." (Page 1)
# =======================================================================
# Between first file attachment and first "Show moreShow less"
# The actual user text starts after "Pasted markdown (2)(1).md File" and the blank line
p001_match = re.search(r"Pasted markdown \(2\)\(1\)\.md\s+File\s+(Make this prompt better.*?)Show moreShow less", raw_full, re.DOTALL)
if p001_match:
    user_text = p001_match.group(1).strip()
    header = "SOURCE: Improving Testing Prompt.pdf, Page 1\nTYPE: User Prompt (VERBATIM EXTRACT)\n================================================================================\n\n"
    write_prompt(f"{OUT_DIR}/user/P001_original_testing_prompt_request.txt", header + user_text)
    print(f"P001: {len(user_text)} chars")

# =======================================================================
# P002 — Assistant: "Improved Prompt" / Senior QA Engineer (Pages 1-11)
# =======================================================================
# Between first "Show moreShow less" and "Pasted markdown(6).md" 
p002_match = re.search(r"Show moreShow less\s+(.*?)Pasted markdown\(6\)\.md", raw_full, re.DOTALL)
if p002_match:
    text = p002_match.group(1).strip()
    text = strip_page_annotations(text)
    # Remove the opening "Here is a substantially improved version..." paragraph
    # Actually the prompt starts with "Improved Prompt" heading
    # Let's keep everything after "Show moreShow less" until "Pasted markdown(6).md"
    # But also remove "Pasted markdownPasted markdown (2)" noise
    text = re.sub(r"Pasted markdownPasted markdown \(2\)\n?", "", text)
    text = re.sub(r"Pasted markdown\(6\)", "", text)
    text = text.strip()
    header = "SOURCE: Improving Testing Prompt.pdf, Pages 1-11\nTYPE: Assistant-Generated Agent Prompt (VERBATIM EXTRACT)\n================================================================================\n\n"
    write_prompt(f"{OUT_DIR}/assistant/P002_improved_testing_prompt_senior_qa.txt", header + text)
    print(f"P002: {len(text)} chars")

# =======================================================================
# P003 — User: "I got this report now I want you to build me an agent..." (Pages 11-12)
# =======================================================================
# After "Pasted markdown(6).md File" until next "Show moreShow less"
p003_match = re.search(r"Pasted markdown\(6\)\.md\s+File\s+(I got this report.*?)Show moreShow less", raw_full, re.DOTALL)
if p003_match:
    text = p003_match.group(1).strip()
    text = re.sub(r"Printed using ChatGPT.*?\n", "", text)
    text = text.strip()
    header = "SOURCE: Improving Testing Prompt.pdf, Pages 11-12\nTYPE: User Prompt (VERBATIM EXTRACT)\n================================================================================\n\n"
    write_prompt(f"{OUT_DIR}/user/P003_bug_fixing_agent_request.txt", header + text)
    print(f"P003: {len(text)} chars")

# =======================================================================
# P004 — Assistant: Bug-fixing agent (Pages 12-13)
# =======================================================================
# After second "Show moreShow less" until "Pasted text(10).txt Document"
p004_match = re.search(r"Show moreShow less\s+(You are a senior software engineer.*?)Pasted text\(10\)\.txt\s+Document", raw_full, re.DOTALL)
if p004_match:
    text = p004_match.group(1).strip()
    text = strip_page_annotations(text)
    text = re.sub(r"Pasted markdownPasted markdown\n?", "", text)
    text = text.strip()
    header = "SOURCE: Improving Testing Prompt.pdf, Pages 12-13\nTYPE: Assistant-Generated Agent Prompt (VERBATIM EXTRACT)\n================================================================================\n\n"
    write_prompt(f"{OUT_DIR}/assistant/P004_bug_fixing_agent_prompt.txt", header + text)
    print(f"P004: {len(text)} chars")

# =======================================================================
# P005 — User: "I got this report now and now I want an agent..." (Pages 13-16)
# =======================================================================
p005_match = re.search(r"Pasted text\(10\)\.txt\s+Document\s+(I got this report now and now I want.*?)Show moreShow less", raw_full, re.DOTALL)
if p005_match:
    text = p005_match.group(1).strip()
    text = strip_page_annotations(text)
    text = text.strip()
    header = "SOURCE: Improving Testing Prompt.pdf, Pages 13-16\nTYPE: User Prompt (VERBATIM EXTRACT)\n================================================================================\n\n"
    write_prompt(f"{OUT_DIR}/user/P005_retesting_agent_request.txt", header + text)
    print(f"P005: {len(text)} chars")

# =======================================================================
# P006 — Assistant: Retesting agent (Pages 14-16)
# =======================================================================
p006_match = re.search(r"Show moreShow less\s+(You are a senior QA automation.*?)Pasted text", raw_full, re.DOTALL)
if p006_match:
    text = p006_match.group(1).strip()
    text = strip_page_annotations(text)
    text = text.strip()
    header = "SOURCE: Improving Testing Prompt.pdf, Pages 14-16\nTYPE: Assistant-Generated Agent Prompt (VERBATIM EXTRACT)\n================================================================================\n\n"
    write_prompt(f"{OUT_DIR}/assistant/P006_retesting_agent_prompt.txt", header + text)
    print(f"P006: {len(text)} chars")

# =======================================================================
# P007 — User: "I want you to build be an agent for this task only..." (Pages 16-20)
# =======================================================================
p007_match = re.search(r"Pasted text\s+(I want you to build be an agent.*?)Show moreShow less", raw_full, re.DOTALL)
if p007_match:
    text = p007_match.group(1).strip()
    text = strip_page_annotations(text)
    text = text.strip()
    header = "SOURCE: Improving Testing Prompt.pdf, Pages 16-20\nTYPE: User Prompt (VERBATIM EXTRACT)\n================================================================================\n\n"
    write_prompt(f"{OUT_DIR}/user/P007_wrapper_agent_specific_restrictions.txt", header + text)
    print(f"P007: {len(text)} chars")

print("\nFirst batch complete. Running second batch for remaining chunks...")
