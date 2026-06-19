#!/usr/bin/env python3
"""Batch 5: Corrected extraction for P014-P018 with proper boundary detection."""

import os, re

RAW_DIR = "/home/lightdesk/MyPrompts/extracted_prompts"
OUT = f"{RAW_DIR}/prompts"

def t(file):
    with open(f"{RAW_DIR}/{file}") as f:
        return f.read()

def strip_pages(t):
    return re.sub(r"\n?Printed using ChatGPT to PDF, powered by PDFCrowd HTML to PDF API\. \d+/190\n?", "", t)

txt21 = t("raw_text_21_40.txt")
txt41 = t("raw_text_41_60.txt")

# ===== P014 (Assistant, pages 31-33) =====
# Starts after "Pasted markdown(8).md\nFile" boundary
# P013 user text comes first, then "Show moreShow less", then P014 starts with "You are a senior end-to-end QA agent"
# P014 ends when P015 user text starts with "I want an agent prompt for an agent who will take"
p014_start = "You are a senior end-to-end QA agent for the ZonePilot project."
p015_start = "I want an agent prompt for an agent who will take my current backend"

parts = txt21.split("Pasted markdown(8).md\nFile\n", 1)
if len(parts) > 1:
    after_md8 = parts[1]
    after_md8_stripped = strip_pages(after_md8)
    
    if p014_start in after_md8_stripped:
        splits = after_md8_stripped.split(p014_start, 1)
        p013_text = splits[0].strip()
        p014_rest = p014_start + splits[1]
        
        # P014 ends where P015 starts
        if p015_start in p014_rest:
            p014_text = p014_rest.split(p015_start)[0].strip()
        else:
            p014_text = p014_rest.strip()
        
        with open(f"{OUT}/user/P013_e2e_tester_java_project_request.txt", "w") as f:
            f.write("SOURCE: Improving Testing Prompt.pdf, Pages 30-31\nTYPE: User Prompt (VERBATIM EXTRACT)\n================================================================================\n\n" + p013_text)
        print(f"P013: {len(p013_text)} chars")
        with open(f"{OUT}/assistant/P014_senior_e2e_qa_zonepilot_prompt.txt", "w") as f:
            f.write("SOURCE: Improving Testing Prompt.pdf, Pages 31-33\nTYPE: Assistant-Generated Agent Prompt (VERBATIM EXTRACT)\n================================================================================\n\n" + p014_text)
        print(f"P014: {len(p014_text)} chars")

# ===== P015 (User, page 34) + P016 (Assistant, pages 34-38) =====
parts = txt21.split(p015_start, 1)
if len(parts) > 1:
    p015_p016 = p015_start + parts[1]
    p015_p016_stripped = strip_pages(p015_p016)
    
    p016_start = "You are a senior DevOps, cloud deployment, and production infrastructure engineer"
    
    if p016_start in p015_p016_stripped:
        splits = p015_p016_stripped.split(p016_start, 1)
        p015_text = splits[0].strip()
        p016_rest = p016_start + splits[1]
        
        # P016 ends before P017 starts
        p017_start = "I am having bugs where the pg routing"
        if p017_start in p016_rest:
            p016_text = p016_rest.split(p017_start)[0].strip()
        else:
            p016_text = p016_rest.strip()
        
        with open(f"{OUT}/user/P015_deployment_agent_render_vercel_request.txt", "w") as f:
            f.write("SOURCE: Improving Testing Prompt.pdf, Page 34\nTYPE: User Prompt (VERBATIM EXTRACT)\n================================================================================\n\n" + p015_text)
        print(f"P015: {len(p015_text)} chars")
        with open(f"{OUT}/assistant/P016_devops_deployment_engineer_prompt.txt", "w") as f:
            f.write("SOURCE: Improving Testing Prompt.pdf, Pages 34-38\nTYPE: Assistant-Generated Agent Prompt (VERBATIM EXTRACT)\n================================================================================\n\n" + p016_text)
        print(f"P016: {len(p016_text)} chars")

# ===== P017 (User, page 38) + P018 (Assistant, pages 38-41) =====
parts = txt21.split(p017_start, 1)
if len(parts) > 1:
    p017_p018 = p017_start + parts[1]
    p017_p018_stripped = strip_pages(p017_p018)
    
    p018_start = "You are a senior full-stack debugging and implementation agent for the ZonePilot project."
    
    if p018_start in p017_p018_stripped:
        splits = p017_p018_stripped.split(p018_start, 1)
        p017_text = splits[0].strip()
        p018_text = (p018_start + splits[1]).strip()
        
        with open(f"{OUT}/user/P017_pgrouting_simulation_bug_fix_request.txt", "w") as f:
            f.write("SOURCE: Improving Testing Prompt.pdf, Page 38\nTYPE: User Prompt (VERBATIM EXTRACT)\n================================================================================\n\n" + p017_text)
        print(f"P017: {len(p017_text)} chars")
        with open(f"{OUT}/assistant/P018_senior_fullstack_debugging_prompt.txt", "w") as f:
            f.write("SOURCE: Improving Testing Prompt.pdf, Pages 38-41\nTYPE: Assistant-Generated Agent Prompt (VERBATIM EXTRACT)\n================================================================================\n\n" + p018_text)
        print(f"P018: {len(p018_text)} chars")

# ===== P019 (User, page 42): "I want an agent who will help me ideate..." =====
# In txt41 (raw_text_41_60.txt)
anchor = "I want an agent who will help me ideate and come up with a methodical approach to this project"
if anchor in txt41:
    p019_p020 = txt41.split(anchor, 1)
    p019 = anchor + p019_p020[1].split("\n# Role")[0]  # Stop before the assistant's response starts
    p019 = strip_pages(p019)
    p019 = p019.strip()
    with open(f"{OUT}/user/P019_ideation_planning_agent_request.txt", "w") as f:
        f.write("SOURCE: Improving Testing Prompt.pdf, Page 42\nTYPE: User Prompt (VERBATIM EXTRACT)\n================================================================================\n\n" + p019)
    print(f"P019: {len(p019)} chars")

# ===== P020 (User, page 43): "I want you to give me an agent prompt for that task..." =====
anchor = "I want you to give me an agent prompt for that task rather than you acting as an agent"
if anchor in txt41:
    p020 = anchor
    p020 = p020.strip()
    with open(f"{OUT}/user/P020_specific_agent_prompt_request.txt", "w") as f:
        f.write("SOURCE: Improving Testing Prompt.pdf, Page 43\nTYPE: User Prompt (VERBATIM EXTRACT)\n================================================================================\n\n" + p020)
    print(f"P020: {len(p020)} chars")

# ===== P021 (Assistant, pages 43-49) =====
anchor = "You are a world-class systems architect, technical strategist, and product planning expert"
if anchor in txt41:
    p021 = anchor + txt41.split(anchor, 1)[1]
    # End before "Pasted markdown(11).md" if it exists, or "Pasted markdown(12)"
    for end_marker in ["Pasted markdown(11).md", "Pasted markdown(12)"]:
        if end_marker in p021:
            p021 = p021.split(end_marker)[0]
    p021 = strip_pages(p021)
    p021 = p021.strip()
    with open(f"{OUT}/assistant/P021_systems_architect_planner_prompt.txt", "w") as f:
        f.write("SOURCE: Improving Testing Prompt.pdf, Pages 43-49\nTYPE: Assistant-Generated Agent Prompt (VERBATIM EXTRACT)\n================================================================================\n\n" + p021)
    print(f"P021: {len(p021)} chars")

print("Done batch 5")
