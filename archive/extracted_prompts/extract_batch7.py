#!/usr/bin/env python3
"""Batch 7: Extract P035-P051 assistant prompts from raw_text_81_100.txt and raw_text_101_120.txt"""

import os, re

RAW_DIR = "/home/lightdesk/MyPrompts/extracted_prompts"
OUT = f"{RAW_DIR}/prompts"

def strip_pages(t):
    t = re.sub(r"\n?Printed using ChatGPT to PDF, powered by PDFCrowd HTML to PDF API\. \d+/190\n?", "\n", t)
    return re.sub(r"\n={2,}\nPAGE \d+\n={2,}\n", "\n", t)

def extract_assistant(raw_text, anchor, fname, src_pages, end_marker=None):
    if anchor not in raw_text:
        print(f"  MISSING: {anchor[:80]}")
        return False
    after = raw_text.split(anchor, 1)[1]
    result = anchor + after
    if end_marker and end_marker in result:
        result = result.split(end_marker)[0]
    if "Show moreShow less" in result:
        result = result.split("Show moreShow less")[0]
    result = strip_pages(result).strip()
    outpath = f"{OUT}/assistant/{fname}"
    with open(outpath, "w") as f:
        f.write(f"SOURCE: Improving Testing Prompt.pdf, {src_pages}\nTYPE: Assistant-Generated Agent Prompt (VERBATIM EXTRACT)\n================================================================================\n\n{result}")
    print(f"  {fname}: {len(result)} chars")
    return True

c81 = open(f"{RAW_DIR}/raw_text_81_100.txt").read()
c101 = open(f"{RAW_DIR}/raw_text_101_120.txt").read()

# P035: Academic Report Creator (pages 81-84)
print("=== P035 ===")
extract_assistant(c81,
    "You are an academic project report creator agent for the ZonePilot project.",
    "P035_academic_report_creator_prompt.txt",
    "Pages 81-84",
    end_marker="I want an agent for creating this report now I will give it the questions")

# P037: LeetCode Report Agent (pages 85-87)
print("=== P037 ===")
extract_assistant(c81,
    "You are a senior academic report drafting agent for a BMSIT mini-project / LeetCode submission.",
    "P037_leetcode_report_agent_prompt.txt",
    "Pages 85-87",
    end_marker="My current agent for teaching and asking questions for learning topics while building projects")

# P039: Learning Coach / Tutor (pages 88-92)
print("=== P039 ===")
extract_assistant(c81,
    "You are an expert learning coach, technical tutor, and accuracy-first educational guide.",
    "P039_learning_coach_tutor_prompt.txt",
    "Pages 88-92",
    end_marker="Give me an agent who can analyse and give me the cause of it")

# P041: LLM Runtime Debug Engineer (pages 92-95)
print("=== P041 ===")
extract_assistant(c81,
    "You are a senior LLM runtime debugging and integration engineer.",
    "P041_llm_runtime_debug_engineer_prompt.txt",
    "Pages 92-95",
    end_marker="I want you to build me agent for opensource contribution PR analyser")

# P043: Open-Source PR Analyst (pages 95-99)
print("=== P043 ===")
extract_assistant(c81,
    "You are a senior open-source contributor, pull request strategist, and repository triage analyst.",
    "P043_opensource_pr_analyst_prompt.txt",
    "Pages 95-99",
    end_marker="You are a senior open-source bug hunter, full-stack debugger, and PR-quality analyst.")

# Hidden: Open-Source Bug Hunter (pages 100-103) - not in manifest but identified
print("=== P043b: Bug Hunter (pages 100-103) ===")
extract_assistant(c81,
    "You are a senior open-source bug hunter, full-stack debugger, and PR-quality analyst.",
    "P043b_bug_hunter_agent_prompt.txt",
    "Pages 100-103",
    end_marker="Give me an agent prompt to write me a report for an event.")

# P045: Cultural Report Producer (page 104) - Note: NO "You are" anchor exists
# The assistant gave conversational advice, not a structured agent prompt
# Mark as "no agent prompt generated"
print("=== P045: NO AGENT PROMPT (conversational only) ===")
with open(f"{OUT}/assistant/P045_NO_AGENT_PROMPT_GENERATED.txt", "w") as f:
    f.write("SOURCE: Improving Testing Prompt.pdf, Page 104\n")
    f.write("TYPE: Assistant-Generated Agent Prompt (VERBATIM EXTRACT)\n")
    f.write("NOTE: The assistant provided conversational advice/analysis rather than\n")
    f.write("a structured 'You are' agent prompt for this use case.\n")
    f.write("================================================================================\n\n")
    f.write("NO AGENT PROMPT GENERATED — conversational response only.\n")
    f.write("The assistant analyzed the cultural report format and gave implementation\n")
    f.write("advice but did not produce a reusable agent prompt template.\n")
print("  P045: No agent prompt (conversational only)")

# P047: Fridge Buying Analyst (pages 105-109)
print("=== P047 ===")
extract_assistant(c101,
    "You are a senior appliance buying analyst, consumer-tech researcher, and decision strategist.",
    "P047_fridge_buying_analyst_prompt.txt",
    "Pages 105-109",
    end_marker="give me an agent prompt who is an expert in cloudflare")

# P049: Cloud Infrastructure Architect (pages 109-115)
print("=== P049 ===")
extract_assistant(c101,
    "You are a senior cloud infrastructure architect, security engineer, and containerized self-hosting specialist.",
    "P049_cloud_infrastructure_architect_prompt.txt",
    "Pages 109-115",
    end_marker="I want an agent prompt to write me these programs in python")

# P051: Lab Report Production Agent (pages 116-120)
# NOTE: This spans chunk6 and continues into chunk7 (page 120+)
# Concatenate for completeness
print("=== P051 ===")
c101_121 = c101 + "\n" + open(f"{RAW_DIR}/raw_text_121_140.txt").read()
extract_assistant(c101_121,
    "You are a senior academic programming assistant, Python automation engineer, and PDF report production specialist.",
    "P051_lab_report_production_prompt.txt",
    "Pages 116-120",
    end_marker="i want an agent to investigate a bug")

print("Done batch 7")
