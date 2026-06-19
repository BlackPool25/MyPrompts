#!/usr/bin/env python3
"""Batch 3: Prompts from raw_text_21_40.txt and raw_text_41_60.txt"""

import os, re

RAW_DIR = "/home/lightdesk/MyPrompts/extracted_prompts"
OUT = f"{RAW_DIR}/prompts"

def t(file):
    with open(f"{RAW_DIR}/{file}") as f:
        return f.read()

def strip_pages(t):
    return re.sub(r"\n?Printed using ChatGPT to PDF, powered by PDFCrowd HTML to PDF API\. \d+/190\n?", "", t)

# ===== P009 (User, page 21) =====
# "Give me an agent who will do rigorous testing..."
txt = t("raw_text_21_40.txt")
p009 = txt.split("Give me an agent who will do rigirous testing", 1)
if len(p009) > 1:
    p009 = "Give me an agent who will do rigirous testing" + p009[1]
    p009 = p009.split("Show moreShow less")[0]
    p009 = strip_pages(p009)
    p009 = p009.strip()
    with open(f"{OUT}/user/P009_rigorous_testing_all_features_request.txt", "w") as f:
        f.write("SOURCE: Improving Testing Prompt.pdf, Page 21\nTYPE: User Prompt (VERBATIM EXTRACT)\n================================================================================\n\n" + p009)
    print(f"P009: {len(p009)} chars")

# ===== P010 (Assistant, pages 21-24) =====
p010 = txt.split("Show moreShow less\nYou are a senior software testing agent", 1)
if len(p010) > 1:
    p010 = "You are a senior software testing agent" + p010[1]
    p010 = p010.split("Pasted markdown(7).md")[0]
    p010 = strip_pages(p010)
    p010 = p010.strip()
    with open(f"{OUT}/assistant/P010_senior_testing_agent_prompt.txt", "w") as f:
        f.write("SOURCE: Improving Testing Prompt.pdf, Pages 21-24\nTYPE: Assistant-Generated Agent Prompt (VERBATIM EXTRACT)\n================================================================================\n\n" + p010)
    print(f"P010: {len(p010)} chars")

# ===== P011 (User, page 24) =====
p011 = txt.split("Pasted markdown(7).md\nFile\nGive me an end to end tester agent prompt", 1)
if len(p011) > 1:
    p011 = "Give me an end to end tester agent prompt" + p011[1]
    p011 = p011.split("Show moreShow less")[0]
    p011 = strip_pages(p011)
    p011 = p011.strip()
    with open(f"{OUT}/user/P011_e2e_tester_workflow_system_request.txt", "w") as f:
        f.write("SOURCE: Improving Testing Prompt.pdf, Page 24\nTYPE: User Prompt (VERBATIM EXTRACT)\n================================================================================\n\n" + p011)
    print(f"P011: {len(p011)} chars")

# ===== P012 (Assistant, pages 24-30) =====
p012 = txt.split("Show moreShow less\nYou are a principal-level end-to-end systems QA", 1)
if len(p012) > 1:
    p012 = "You are a principal-level end-to-end systems QA" + p012[1]
    p012 = p012.split("Pasted markdown(8).md")[0]
    p012 = strip_pages(p012)
    p012 = p012.strip()
    with open(f"{OUT}/assistant/P012_principal_e2e_qa_workflow_prompt.txt", "w") as f:
        f.write("SOURCE: Improving Testing Prompt.pdf, Pages 24-30\nTYPE: Assistant-Generated Agent Prompt (VERBATIM EXTRACT)\n================================================================================\n\n" + p012)
    print(f"P012: {len(p012)} chars")

# ===== P013 (User, pages 30-31) =====
p013 = txt.split("Pasted markdown(8).md\nFile\nGive me an E2E tester agent prompt", 1)
if len(p013) > 1:
    p013 = "Give me an E2E tester agent prompt" + p013[1]
    p013 = p013.split("Show moreShow less")[0]
    p013 = strip_pages(p013)
    p013 = p013.strip()
    with open(f"{OUT}/user/P013_e2e_tester_java_project_request.txt", "w") as f:
        f.write("SOURCE: Improving Testing Prompt.pdf, Pages 30-31\nTYPE: User Prompt (VERBATIM EXTRACT)\n================================================================================\n\n" + p013)
    print(f"P013: {len(p013)} chars")

# ===== P014 (Assistant, pages 31-33) =====
p014 = txt.split("Show moreShow less\nYou are a senior end-to-end QA agent", 1)
if len(p014) > 1:
    p014 = "You are a senior end-to-end QA agent" + p014[1]
    # End at end of this chunk or next marker
    p014 = p014.strip()
    p014 = strip_pages(p014)
    with open(f"{OUT}/assistant/P014_senior_e2e_qa_zonepilot_prompt.txt", "w") as f:
        f.write("SOURCE: Improving Testing Prompt.pdf, Pages 31-33\nTYPE: Assistant-Generated Agent Prompt (VERBATIM EXTRACT)\n================================================================================\n\n" + p014)
    print(f"P014: {len(p014)} chars")

# ===== P015 (User, page 34) =====
txt2 = t("raw_text_41_60.txt")
p015 = txt2.split("I want an agent prompt for an agent who will take my current backend", 1)
if len(p015) > 1:
    p015 = "I want an agent prompt for an agent who will take my current backend" + p015[1]
    p015 = p015.split("Show moreShow less")[0]
    p015 = strip_pages(p015)
    p015 = p015.strip()
    with open(f"{OUT}/user/P015_deployment_agent_render_vercel_request.txt", "w") as f:
        f.write("SOURCE: Improving Testing Prompt.pdf, Page 34\nTYPE: User Prompt (VERBATIM EXTRACT)\n================================================================================\n\n" + p015)
    print(f"P015: {len(p015)} chars")

# ===== P016 (Assistant, pages 34-38) =====
p016 = txt2.split("Show moreShow less\nYou are a senior DevOps, cloud deployment", 1)
if len(p016) > 1:
    p016 = "You are a senior DevOps, cloud deployment" + p016[1]
    p016 = p016.split("Pasted markdown(10).md")[0]
    p016 = strip_pages(p016)
    p016 = p016.strip()
    with open(f"{OUT}/assistant/P016_devops_deployment_engineer_prompt.txt", "w") as f:
        f.write("SOURCE: Improving Testing Prompt.pdf, Pages 34-38\nTYPE: Assistant-Generated Agent Prompt (VERBATIM EXTRACT)\n================================================================================\n\n" + p016)
    print(f"P016: {len(p016)} chars")

# ===== P017 (User, page 38) =====
p017 = txt2.split("Pasted markdown(10).md\nFile\nI am having bugs where the pg routing", 1)
if len(p017) > 1:
    p017 = "I am having bugs where the pg routing" + p017[1]
    p017 = p017.split("Show moreShow less")[0]
    p017 = strip_pages(p017)
    p017 = p017.strip()
    with open(f"{OUT}/user/P017_pgrouting_simulation_bug_fix_request.txt", "w") as f:
        f.write("SOURCE: Improving Testing Prompt.pdf, Page 38\nTYPE: User Prompt (VERBATIM EXTRACT)\n================================================================================\n\n" + p017)
    print(f"P017: {len(p017)} chars")

# ===== P018 (Assistant, pages 38-41) =====
p018 = txt2.split("Show moreShow less\nYou are a senior full-stack debugging", 1)
if len(p018) > 1:
    p018 = "You are a senior full-stack debugging" + p018[1]
    p018 = p018.strip()
    p018 = strip_pages(p018)
    with open(f"{OUT}/assistant/P018_senior_fullstack_debugging_prompt.txt", "w") as f:
        f.write("SOURCE: Improving Testing Prompt.pdf, Pages 38-41\nTYPE: Assistant-Generated Agent Prompt (VERBATIM EXTRACT)\n================================================================================\n\n" + p018)
    print(f"P018: {len(p018)} chars")

print("Done batch 3")
