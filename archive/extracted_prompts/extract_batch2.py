#!/usr/bin/env python3
"""Full verbatim prompt extraction - batch 2.
Covers P004 through P008 from raw_text_1_20.txt (pages 12-20)."""

import os, re

CHUNK = "/home/lightdesk/MyPrompts/extracted_prompts/raw_text_1_20.txt"
OUT = "/home/lightdesk/MyPrompts/extracted_prompts/prompts"

with open(CHUNK) as f:
    text = f.read()

def write_prompt(path, content):
    with open(path, "w") as f:
        f.write(content)

def strip_pages(t):
    return re.sub(r"\n?Printed using ChatGPT to PDF, powered by PDFCrowd HTML to PDF API\. \d+/190\n?", "", t)

# ===== P004 (Assistant, pages 12-13) =====
# Starts at "Based on the QA report..." after line 401 "Show moreShow less"
# Ends at "Pasted text(10).txt\nDocument" on line 424
p004 = text.split("Show moreShow less\n")[1]  # after first Show more
p004 = p004.split("Pasted text(10).txt\nDocument")[0]  # before next attachment
p004 = strip_pages(p004)
p004 = re.sub(r"Pasted markdownPasted markdown\n?", "", p004)
p004 = p004.strip()
h = "SOURCE: Improving Testing Prompt.pdf, Pages 12-13\nTYPE: Assistant-Generated Agent Prompt (VERBATIM EXTRACT)\n================================================================================\n\n"
write_prompt(f"{OUT}/assistant/P004_bug_fixing_agent_prompt.txt", h + p004)
print(f"P004: {len(p004)} chars")

# ===== P005 (User, pages 13) =====
# After "Pasted text(10).txt\nDocument" until "Pasted text" on line 443
# User says "I got this report now and now I want an agent who will do the testing again..."
# Then the assistant response starts (P006)
p005_parts = text.split("Pasted text(10).txt\nDocument\n", 1)
if len(p005_parts) > 1:
    p005 = p005_parts[1]
    # The user message is just the first line "I got this report now..."
    # until the assistant response starts
    user_p005 = p005.split("This prompt is designed to")[0]
    user_p005 = strip_pages(user_p005)
    user_p005 = user_p005.strip()
    h = "SOURCE: Improving Testing Prompt.pdf, Pages 13\nTYPE: User Prompt (VERBATIM EXTRACT)\n================================================================================\n\n"
    write_prompt(f"{OUT}/user/P005_retesting_agent_request.txt", h + user_p005)
    print(f"P005: {len(user_p005)} chars")

# ===== P006 (Assistant, pages 13-16) =====
# Starts after "This prompt is designed to retest..." lead-in
# The actual prompt starts with "You are a senior QA automation..."
# Ends at "I want you to build be an agent..." on line 465
p006_parts = text.split("This prompt is designed to retest", 1)
if len(p006_parts) > 1:
    p006 = "This prompt is designed to retest" + p006_parts[1]
    p006 = p006.split("\nI want you to build be an agent")[0]
    p006 = strip_pages(p006)
    p006 = re.sub(r"Pasted text\n?", "", p006)
    p006 = p006.strip()
    h = "SOURCE: Improving Testing Prompt.pdf, Pages 13-16\nTYPE: Assistant-Generated Agent Prompt (VERBATIM EXTRACT)\n================================================================================\n\n"
    write_prompt(f"{OUT}/assistant/P006_retesting_agent_prompt.txt", h + p006)
    print(f"P006: {len(p006)} chars")

# ===== P007 (User, pages 16-20) =====
# The user's P007 message: "I want you to build be an agent for this task only..."
# along with the attached "# Role & Goal" through "# Output Instructions"
# Ends at "Show moreShow less" on line 531
p007_parts = text.split("\nI want you to build be an agent for this task only prompt", 1)
if len(p007_parts) > 1:
    p007 = "I want you to build be an agent for this task only prompt" + p007_parts[1]
    p007 = p007.split("Show moreShow less")[0]
    p007 = strip_pages(p007)
    p007 = p007.strip()
    h = "SOURCE: Improving Testing Prompt.pdf, Pages 16-20\nTYPE: User Prompt (VERBATIM EXTRACT)\n================================================================================\n\n"
    write_prompt(f"{OUT}/user/P007_wrapper_agent_specific_restrictions.txt", h + p007)
    print(f"P007: {len(p007)} chars")

# ===== P008 (Assistant, pages 17-20) =====
# Starts at "You are a principal-level geospatial systems engineer..."
# after the "Show moreShow less" on line 531
# Ends at the end of page 20 (end of first chunk)
p008 = text.split("Show moreShow less\nYou are a principal-level", 1)
if len(p008) > 1:
    p008 = "You are a principal-level" + p008[1]
    # Remove any trailing page noise
    p008 = p008.strip()
    p008 = strip_pages(p008)
    h = "SOURCE: Improving Testing Prompt.pdf, Pages 17-20\nTYPE: Assistant-Generated Agent Prompt (VERBATIM EXTRACT)\n================================================================================\n\n"
    write_prompt(f"{OUT}/assistant/P008_principal_geospatial_engineer_prompt.txt", h + p008)
    print(f"P008: {len(p008)} chars")

print("Done batch 2")
