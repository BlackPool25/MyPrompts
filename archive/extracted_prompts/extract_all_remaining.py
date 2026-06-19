#!/usr/bin/env python3
"""Extract all remaining assistant prompts from all raw text chunks."""

import os, re

RAW_DIR = "/home/lightdesk/MyPrompts/extracted_prompts"
OUT = f"{RAW_DIR}/prompts"

def strip_pages(t):
    return re.sub(r"\n?Printed using ChatGPT to PDF, powered by PDFCrowd HTML to PDF API\. \d+/190\n?", "\n", t)

def strip_page_headers(t):
    return re.sub(r"\n={2,}\nPAGE \d+\n={2,}\n", "\n", t)

def clean(text):
    text = strip_pages(text)
    text = strip_page_headers(text)
    return text.strip()

def extract_assistant(raw_text, anchor, fname, src_pages, end_marker=None):
    if anchor not in raw_text:
        print(f"  MISSING anchor: {anchor[:80]}")
        return False
    after = raw_text.split(anchor, 1)[1]
    result = anchor + after
    
    if end_marker and end_marker in result:
        result = result.split(end_marker)[0]
    
    # Also try to cut at "Show moreShow less" if end_marker not specified
    if not end_marker and "Show moreShow less" in result:
        result = result.split("Show moreShow less")[0]
    
    result = clean(result)
    
    outpath = f"{OUT}/assistant/{fname}"
    with open(outpath, "w") as f:
        f.write(f"SOURCE: Improving Testing Prompt.pdf, {src_pages}\nTYPE: Assistant-Generated Agent Prompt (VERBATIM EXTRACT)\n================================================================================\n\n{result}")
    print(f"  {fname}: {len(result)} chars")
    return True

def load_chunk(name):
    return open(f"{RAW_DIR}/{name}").read()

# ============================================================================
# Chunks
# ============================================================================
c41 = load_chunk("raw_text_41_60.txt")
c61 = load_chunk("raw_text_61_80.txt")
c81 = load_chunk("raw_text_81_100.txt")
c101 = load_chunk("raw_text_101_120.txt")
c121 = load_chunk("raw_text_121_140.txt")
c141 = load_chunk("raw_text_141_160.txt")
c161 = load_chunk("raw_text_161_180.txt")
c181 = load_chunk("raw_text_181_190.txt")

# ============================================================================
# P023: Database Recovery Agent (pages 49-54)
# Anchor in chunk3, continues into chunk4
# Use P024 user text as end marker
# ============================================================================
print("=== P023 ===")
c3_4 = c41 + "\n" + c61  # Concatenate in case response spans both
extract_assistant(c3_4,
    "You are a senior database recovery, reverse-engineering, and Supabase/Postgres architecture agent.",
    "P023_database_recovery_agent_prompt.txt",
    "Pages 49-54",
    end_marker="I need an agent to test this Project end to end.")

# ============================================================================
# P027: Frontend Architect Refactor (pages 61-66)
# Anchor in chunk4
# Use P028 user anchor as end marker
# ============================================================================
print("=== P027 ===")
extract_assistant(c61,
    "You are a senior frontend architect, full-stack integration engineer, and product-quality implementation agent for PolicySattva.",
    "P027_frontend_architect_refactor_prompt.txt",
    "Pages 61-66",
    end_marker="I want an agent to create me a background image to use in my hero section")

# ============================================================================
# P031: RAG Performance Debugger (pages 70-74)
# Anchor in chunk4
# Use P032 user anchor as end marker
# ============================================================================
print("=== P031 ===")
extract_assistant(c61,
    "You are a senior AI systems engineer, RAG architect, and performance debugging specialist for PolicySattva.",
    "P031_rag_performance_debugger_prompt.txt",
    "Pages 70-74",
    end_marker="So I am trying to get an internship")

# ============================================================================
# P035: Academic Report Creator (pages 81-84)
# Anchor in chunk5
# ============================================================================
print("=== P035 ===")
extract_assistant(c81,
    "You are an academic project report creator agent for the ZonePilot project.",
    "P035_academic_report_creator_prompt.txt",
    "Pages 81-84",
    end_marker="I want an agent for creating this report now I will give it the questions")

# ============================================================================
# P037: LeetCode Report Agent (pages 85-87)
# ============================================================================
print("=== P037 ===")
extract_assistant(c81,
    "You are an academic report creator for a real mini project submission.",
    "P037_leetcode_report_agent_prompt.txt",
    "Pages 85-87",
    end_marker="I want you to build me an agent who can be a agent that teaches")

# ============================================================================
# P039: Learning Coach / Tutor (pages 88-92)
# ============================================================================
print("=== P039 ===")
extract_assistant(c81,
    "You are an expert learning coach, technical tutor, and accuracy-first educational guide.",
    "P039_learning_coach_tutor_prompt.txt",
    "Pages 88-92",
    end_marker="Give me an agent who can analyse and give me the cause of it")

# ============================================================================
# P041: LLM Runtime Debug Engineer (pages 92-95)
# ============================================================================
print("=== P041 ===")
extract_assistant(c81,
    "You are a senior LLM runtime debugging and integration engineer.",
    "P041_llm_runtime_debug_engineer_prompt.txt",
    "Pages 92-95",
    end_marker="I want you to build me agent for opensource contribution PR analyser")

# ============================================================================
# P043: Open-Source PR Analyst (pages 95-99)
# Also includes "You are an open-source PR analyst and contribution strategist." and
# "You are a senior open-source bug hunter..." (hidden page-100 pair)
# ============================================================================
print("=== P043 ===")
extract_assistant(c81,
    "You are a senior open-source contributor, pull request strategist, and repository triage analyst.",
    "P043_opensource_pr_analyst_prompt.txt",
    "Pages 95-99",
    end_marker="Give me prompt for an agent who will help me find the issue")

# ============================================================================
# Hidden: Bug Hunter Agent (pages 100-103)
# This pair was missed in the manifest
# ============================================================================
print("=== Hidden: Bug Hunter Agent (page 100-103) ===")
extract_assistant(c81,
    "You are a senior open-source bug hunter, full-stack debugger, and PR-quality analyst.",
    "P043b_bug_hunter_agent_prompt.txt",
    "Pages 100-103",
    end_marker="Give me an agent prompt to write me a report for an event.")

# ============================================================================
# P045: PDF Report Production - Cultural (page 104 only)
# The assistant prompt seems very short - page 104 only
# ============================================================================
print("=== P045 ===")
extract_assistant(c101,
    "You are a senior appliance buying analyst, consumer-tech researcher, and decision strategist.",
    "P045_cultural_report_producer_prompt.txt",
    "Page 104",
    end_marker="Okayy so I have to buy a fridge in india")

# Hmm, wait. P045 might be very short. Let me use the generic end marker approach.
# Actually, looking at the manifest: P045 = Assistant, Page 104 = "PDF Report Production Agent"
# But the anchor text "You are a senior appliance buying analyst..." matches P047 (fridge buying).
# Let me re-examine...

# From the raw text, the flow seems to be:
# Pages 100-103: Bug hunter pair (user + assistant)
# Page 104: "Give me an agent prompt to write me a report for an event" (P044 user) + P045 assistant
# Page 104-105: "Okayy so I have to buy a fridge..." (P046 user)

# But the anchor at L103 says "You are a senior appliance buying analyst" which seems like P047
# (fridge buying agent), not P045 (report producer). Let me check what P045 should be.

# Since P045 follows P044 (cultural report request), it should be about PDF report production.
# Let me look for a "You are" related to reportlab / PDF report around page 104.

print("\n=== Searching for P045 anchor (PDF report producer) ===")
for i, line in enumerate(c101.split('\n'), 1):
    if 'report' in line.lower() and ('you are' in line.lower() or 'your job' in line.lower()):
        print(f"  L{i}: {line[:120]}")

# ============================================================================
# P047: Fridge Buying Analyst (pages 105-109)
# ============================================================================
print("\n=== P047 ===")
extract_assistant(c101,
    "You are a senior appliance buying analyst, consumer-tech researcher, and decision strategist.",
    "P047_fridge_buying_analyst_prompt.txt",
    "Pages 105-109",
    end_marker="I want an agent prompt for a cloudflare and authentik infrastructure")
