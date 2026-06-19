#!/usr/bin/env python3
"""Batch 4: Corrected extraction for prompts P009-P018 using 'You are a...' anchors."""

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
txt_combined = txt21 + "\n" + txt41

# Split by "Pasted markdown" markers to find boundaries
# P009 ends at "Pasted markdown(7).md"
# P010 starts after P009 ends, goes until "Pasted markdown(7).md\nFile\nGive me..."
# P011 starts at "Give me an end to end tester agent..."
# P011 ends at "Pasted markdown(8).md"
# P012 starts after P011, goes until "Pasted markdown(8).md\nFile\nGive me an E2E..."
# P013 starts at "Give me an E2E tester agent prompt..."
# P013 ends at "Pasted markdown(10).md"
# etc.

# P009 (User) + P010 (Assistant): Between page 21 and "Pasted markdown(7).md"
# These two have NO Show more separator between them
p009_p010 = txt21.split("Pasted markdown(7).md")[0]
p009_p010 = strip_pages(p009_p010)
# P009 is the first line "Give me an agent who will do rigirous testing..."
# P010 starts immediately after with "You are a senior software testing agent..."
p009_p010_lines = p009_p010.split("\n")
p009_text = ""
p010_text = ""
in_p010 = False
for line in p009_p010_lines:
    if line.startswith("You are a senior software testing agent"):
        in_p010 = True
    if in_p010:
        p010_text += line + "\n"
    else:
        p009_text += line + "\n"

p009_text = p009_text.strip()
p010_text = p010_text.strip()

with open(f"{OUT}/user/P009_rigorous_testing_all_features_request.txt", "w") as f:
    f.write("SOURCE: Improving Testing Prompt.pdf, Page 21\nTYPE: User Prompt (VERBATIM EXTRACT)\n================================================================================\n\n" + p009_text)
print(f"P009: {len(p009_text)} chars")

with open(f"{OUT}/assistant/P010_senior_testing_agent_prompt.txt", "w") as f:
    f.write("SOURCE: Improving Testing Prompt.pdf, Pages 21-24\nTYPE: Assistant-Generated Agent Prompt (VERBATIM EXTRACT)\n================================================================================\n\n" + p010_text)
print(f"P010: {len(p010_text)} chars")

# P011 (User) + P012 (Assistant): Between "Pasted markdown(7).md File" and "Pasted markdown(8).md"
p011_p012 = txt21.split("Pasted markdown(7).md\nFile\n", 1)
if len(p011_p012) > 1:
    p011_p012 = p011_p012[1].split("Pasted markdown(8).md")[0]
    p011_p012 = strip_pages(p011_p012)
    # Find the "You are a principal-level" anchor
    anchor = "You are a principal-level end-to-end systems QA"
    if anchor in p011_p012:
        parts = p011_p012.split(anchor, 1)
        p011_text = parts[0].strip()
        p012_text = (anchor + parts[1]).strip()
        with open(f"{OUT}/user/P011_e2e_tester_workflow_system_request.txt", "w") as f:
            f.write("SOURCE: Improving Testing Prompt.pdf, Page 24\nTYPE: User Prompt (VERBATIM EXTRACT)\n================================================================================\n\n" + p011_text)
        print(f"P011: {len(p011_text)} chars")
        with open(f"{OUT}/assistant/P012_principal_e2e_qa_workflow_prompt.txt", "w") as f:
            f.write("SOURCE: Improving Testing Prompt.pdf, Pages 24-30\nTYPE: Assistant-Generated Agent Prompt (VERBATIM EXTRACT)\n================================================================================\n\n" + p012_text)
        print(f"P012: {len(p012_text)} chars")

# P013 (User) + P014 (Assistant): Between "Pasted markdown(8).md File" and end of chunk 2
p013_p014 = txt21.split("Pasted markdown(8).md\nFile\n", 1)
if len(p013_p014) > 1:
    p013_p014 = p013_p014[1]
    # Remove page annotation
    p013_p014 = strip_pages(p013_p014)
    # Find the "You are a senior end-to-end" anchor
    anchor = "You are a senior end-to-end QA agent for the ZonePilot project"
    if anchor in p013_p014:
        parts = p013_p014.split(anchor, 1)
        p013_text = parts[0].strip()
        p014_text = (anchor + parts[1]).split("Pasted markdown(10)")[0].strip() if "Pasted markdown(10)" in parts[1] else (anchor + parts[1]).strip()
        with open(f"{OUT}/user/P013_e2e_tester_java_project_request.txt", "w") as f:
            f.write("SOURCE: Improving Testing Prompt.pdf, Pages 30-31\nTYPE: User Prompt (VERBATIM EXTRACT)\n================================================================================\n\n" + p013_text)
        print(f"P013: {len(p013_text)} chars")
        with open(f"{OUT}/assistant/P014_senior_e2e_qa_zonepilot_prompt.txt", "w") as f:
            f.write("SOURCE: Improving Testing Prompt.pdf, Pages 31-33\nTYPE: Assistant-Generated Agent Prompt (VERBATIM EXTRACT)\n================================================================================\n\n" + p014_text)
        print(f"P014: {len(p014_text)} chars")

# P015 (User) + P016 (Assistant): In chunk 3
# P015: "I want an agent prompt for an agent who will take..."
# P016: "You are a senior DevOps, cloud deployment..."
anchor15 = "I want an agent prompt for an agent who will take my current backend"
anchor16 = "You are a senior DevOps, cloud deployment, and production infrastructure engineer"
p015_p016 = txt41.split(anchor15, 1)
if len(p015_p016) > 1:
    p015_p016 = (anchor15 + p015_p016[1]).split("Pasted markdown(10).md")[0]
    p015_p016 = strip_pages(p015_p016)
    if anchor16 in p015_p016:
        parts = p015_p016.split(anchor16, 1)
        p015_text = parts[0].strip()
        p016_text = (anchor16 + parts[1]).strip()
        with open(f"{OUT}/user/P015_deployment_agent_render_vercel_request.txt", "w") as f:
            f.write("SOURCE: Improving Testing Prompt.pdf, Page 34\nTYPE: User Prompt (VERBATIM EXTRACT)\n================================================================================\n\n" + p015_text)
        print(f"P015: {len(p015_text)} chars")
        with open(f"{OUT}/assistant/P016_devops_deployment_engineer_prompt.txt", "w") as f:
            f.write("SOURCE: Improving Testing Prompt.pdf, Pages 34-38\nTYPE: Assistant-Generated Agent Prompt (VERBATIM EXTRACT)\n================================================================================\n\n" + p016_text)
        print(f"P016: {len(p016_text)} chars")

# P017 (User) + P018 (Assistant): After "Pasted markdown(10).md File"
anchor17 = "I am having bugs where the pg routing"
anchor18 = "You are a senior full-stack debugging and implementation agent for the ZonePilot project"
p017_p018 = txt41.split("Pasted markdown(10).md\nFile\n", 1)
if len(p017_p018) > 1:
    p017_p018 = p017_p018[1]
    p017_p018 = strip_pages(p017_p018)
    # Find until end of chunk or next marker
    if anchor18 in p017_p018:
        parts = p017_p018.split(anchor18, 1)
        p017_text = parts[0].strip()
        p018_text = anchor18 + parts[1]
        with open(f"{OUT}/user/P017_pgrouting_simulation_bug_fix_request.txt", "w") as f:
            f.write("SOURCE: Improving Testing Prompt.pdf, Page 38\nTYPE: User Prompt (VERBATIM EXTRACT)\n================================================================================\n\n" + p017_text)
        print(f"P017: {len(p017_text)} chars")
        with open(f"{OUT}/assistant/P018_senior_fullstack_debugging_prompt.txt", "w") as f:
            f.write("SOURCE: Improving Testing Prompt.pdf, Pages 38-41\nTYPE: Assistant-Generated Agent Prompt (VERBATIM EXTRACT)\n================================================================================\n\n" + p018_text)
        print(f"P018: {len(p018_text)} chars")

print("Done batch 4")
