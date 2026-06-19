#!/usr/bin/env python3
"""Verbatim prompt extractor - copies exact text from raw files to prompt files.
Uses only cut-and-paste from source; no generation or rewriting."""

import os, re

RAW_DIR = "/home/lightdesk/MyPrompts/extracted_prompts"
OUT_DIR = "/home/lightdesk/MyPrompts/extracted_prompts/prompts"

def read_raw(filename):
    with open(os.path.join(RAW_DIR, filename), "r") as f:
        return f.read()

def write_prompt(path, content):
    with open(path, "w") as f:
        f.write(content)

# === P001: User prompt on page 1 ===
# The user's message starts at "Make this prompt better." and ends at "Show moreShow less"
raw = read_raw("raw_text_1_20.txt")
lines = raw.split("\n")

# Find start: "Make this prompt better"
# Find end: "Show moreShow less" (on line 19, 0-indexed line index 18 -> 0-indexed content)
# Actually in the text the user's message is between line 10 ("Make this prompt better...") and line 18 ("Show moreShow less")

# Let me extract based on the PAGE boundaries I see in the text
# P001 is on page 1, between the PAGE marker and "Show moreShow less"

# Find page 1 content
page1_start = raw.find("PAGE 1")
page1_end = raw.find("PAGE 2")

# Extract page 1 text
page1 = raw[page1_start:page1_end] if page1_end > 0 else raw[page1_start:]

# Find the user prompt within page 1 - it starts after file attachment markers and ends at "Show moreShow less"
# Looking at the text: lines 10-18 contain the user prompt
# "Make this prompt better..." through "...based on that read the files if needed."

# Let me split by lines and find exact content
p1_lines = page1.split("\n")
# Find the actual prompt lines
prompt_start = None
prompt_end = None
for i, l in enumerate(p1_lines):
    if "Make this prompt better" in l:
        prompt_start = i
    if "Show moreShow less" in l:
        prompt_end = i
        break

# The user prompt is from prompt_start to prompt_end (exclusive of the Show more line)
user_p1 = "\n".join(p1_lines[prompt_start:prompt_end])
# Strip the trailing page number line if it got included
user_p1 = re.sub(r"\nPrinted using ChatGPT.*$", "", user_p1)

header = f"""SOURCE: Improving Testing Prompt.pdf, Page 1
TYPE: User Prompt (VERBATIM EXTRACT)
================================================================================

"""
write_prompt(f"{OUT_DIR}/user/P001_original_testing_prompt_request.txt", header + user_p1.strip())
print(f"P001 written: {len(user_p1.strip())} chars")

# === P002: Assistant "Improved Prompt" starting on page 1, continuing through page 11 ===
# The assistant's response starts after "Show moreShow less" on page 1
# The assistant prompt starts with "You are acting as a senior software QA engineer..."
# and goes through to the "Important Behavioral Rules" section, ending before the file attachment on page 11

# Let me extract from the first "Show moreShow less" (end of user msg) to the next attachment marker
after_show = page1.split("Show moreShow less", 1)[1] if "Show moreShow less" in page1 else ""

# Now I need to find where P002 ends. Looking at the raw text, P002 goes through pages 1-11
# and ends just before "Pasted markdown(6).md File" on line 387 of the first chunk

# Let me search for "Pasted markdown(6).md" which marks the end of P002
p002_end_marker = "Pasted markdown(6).md"
if p002_end_marker in raw:
    p002_raw = raw.split("Show moreShow less", 1)[1]  # start after first "Show moreShow less"
    p002_raw = p002_raw.split(p002_end_marker)[0]  # end before the next attachment
    # Strip the page number annotations
    p002_raw = re.sub(r"Printed using ChatGPT to PDF, powered by PDFCrowd HTML to PDF API\. \d+/190\n?", "", p002_raw)
    # Trim trailing whitespace
    p002_raw = p002_raw.strip()
    
    header2 = f"""SOURCE: Improving Testing Prompt.pdf, Pages 1-11
TYPE: Assistant-Generated Agent Prompt (VERBATIM EXTRACT)
NOTES: This is the "Improved Prompt" the assistant wrote. Starts after "Show moreShow less" on page 1,
ends before "Pasted markdown(6).md" on page 11.
================================================================================

"""
    write_prompt(f"{OUT_DIR}/assistant/P002_improved_testing_prompt_senior_qa.txt", header2 + p002_raw)
    print(f"P002 written: {len(p002_raw)} chars")
else:
    print("P002 end marker not found")

# === P003: User prompt on pages 11-12 ===
# Starts after "Pasted markdown(6).md File" and ends at the next "Show moreShow less"
# "I got this report now I want you to build me an agent..."

# The user's P003 message starts after the file attachment and ends at "Show moreShow less"
p003_parts = raw.split(p002_end_marker, 1)
if len(p003_parts) > 1:
    after_marker = p003_parts[1]
    # Split at the next "Show moreShow less"
    p003_parts2 = after_marker.split("Show moreShow less", 1)
    user_p3 = p003_parts2[0].strip()
    # Remove "File" and "Pasted markdownPasted markdown" if those are attachment annotations
    user_p3 = re.sub(r"^File\n?", "", user_p3)
    user_p3 = re.sub(r"Pasted markdown.*$", "", user_p3).strip()
    header3 = f"""SOURCE: Improving Testing Prompt.pdf, Pages 11-12
TYPE: User Prompt (VERBATIM EXTRACT)
================================================================================

"""
    write_prompt(f"{OUT_DIR}/user/P003_bug_fixing_agent_request.txt", header3 + user_p3.strip())
    print(f"P003 written: {len(user_p3.strip())} chars")

print("\nFirst 3 prompts extracted. Check output files.")
