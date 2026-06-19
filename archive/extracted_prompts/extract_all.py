#!/usr/bin/env python3
"""
Extract all remaining assistant prompts.
Uses verified "You are" anchors and correct next-user end markers.
"""

import os, re, glob

RAW_DIR = "/home/lightdesk/MyPrompts/extracted_prompts"
OUT = f"{RAW_DIR}/prompts"

def clean(text):
    text = re.sub(r"\n?Printed using ChatGPT to PDF, powered by PDFCrowd HTML to PDF API\. \d+/190\n?", "\n", text)
    text = re.sub(r"\n={2,}\nPAGE \d+\n={2,}\n", "\n", text)
    text = re.sub(r"\nPasted (markdown|text)\(\d+\)\.(md|txt)\nFile\n?", "\n", text)
    return text.strip()

def extract(raw_text, anchor, fname, src_pages, end_marker=None):
    if anchor not in raw_text:
        print(f"  MISSING: {anchor[:80]}")
        return False
    after = raw_text.split(anchor, 1)[1]
    result = anchor + after
    if end_marker and end_marker in result:
        result = result.split(end_marker)[0]
    if "Show moreShow less" in result:
        result = result.split("Show moreShow less")[0]
    result = clean(result)
    if len(result) < 100:
        print(f"  SHORT ({len(result)} chars): {fname}")
    outpath = f"{OUT}/assistant/{fname}"
    with open(outpath, "w") as f:
        f.write(f"SOURCE: Improving Testing Prompt.pdf, {src_pages}\nTYPE: Assistant-Generated Agent Prompt (VERBATIM EXTRACT)\n================================================================================\n\n{result}")
    print(f"  {fname}: {len(result)} chars")
    return True

def mark_no_prompt(fname, src_pages, note=""):
    outpath = f"{OUT}/assistant/{fname}"
    with open(outpath, "w") as f:
        f.write(f"SOURCE: Improving Testing Prompt.pdf, {src_pages}\n")
        f.write("TYPE: Assistant-Generated Agent Prompt (VERBATIM EXTRACT)\n")
        f.write("NOTE: No structured 'You are' agent prompt was generated.\n")
        f.write(f"      {note}\n")
        f.write("================================================================================\n\n")
        f.write("NO AGENT PROMPT GENERATED — conversational response only.\n")
    print(f"  {fname}: NO PROMPT ({note})")

def c(name):
    return open(f"{RAW_DIR}/{name}").read()

# Load chunks
c3 = c("raw_text_41_60.txt")
c4 = c("raw_text_61_80.txt")
c5 = c("raw_text_81_100.txt")
c6 = c("raw_text_101_120.txt")
c7 = c("raw_text_121_140.txt")
c8 = c("raw_text_141_160.txt")
c9 = c("raw_text_161_180.txt")
c10 = c("raw_text_181_190.txt")
c3_4 = c3 + "\n" + c4
c6_7 = c6 + "\n" + c7
c7_8 = c7 + "\n" + c8   # P059 spans both (anchor c7, end_marker c8)
c9_10 = c9 + "\n" + c10  # P075 spans both (anchor c9, end_marker c10)

skip_existing = True

pairs = [
    # (chunk, anchor, fname, pages, end_marker)
    # Batch 6 leftovers
    (c3_4, "You are a senior database recovery, reverse-engineering, and Supabase/Postgres architecture agent.",
     "P023_database_recovery_agent_prompt.txt", "Pages 49-54",
     "I need an agent to test this Project end to end."),
    (c4, "You are a senior frontend architect, full-stack integration engineer, and product-quality implementation agent for PolicySattva.",
     "P027_frontend_architect_refactor_prompt.txt", "Pages 61-66",
     "I want an agent to create me a background image to use in my hero section"),
    (c4, "You are a senior AI systems engineer, RAG architect, and performance debugging specialist for PolicySattva.",
     "P031_rag_performance_debugger_prompt.txt", "Pages 70-74",
     "So I am trying to get an internship and trying to learn everything I need to know for a java/backend"),
    
    # Batch 7: chunks 5-6
    (c5, "You are an academic project report creator agent for the ZonePilot project.",
     "P035_academic_report_creator_prompt.txt", "Pages 81-84",
     "I want an agent for creating this report now I will give it the questions it should create leetcode"),
    (c5, "You are a senior academic report drafting agent for a BMSIT mini-project / LeetCode submission.",
     "P037_leetcode_report_agent_prompt.txt", "Pages 85-87",
     "My current agent for teaching and asking questions for learning topics while building projects is"),
    (c5, "You are an expert learning coach, technical tutor, and accuracy-first educational guide.",
     "P039_learning_coach_tutor_prompt.txt", "Pages 88-92",
     "I was trying to run Qwen3.6:27B model using llama.cpp server but I got error like this"),
    (c5, "You are a senior LLM runtime debugging and integration engineer.",
     "P041_llm_runtime_debug_engineer_prompt.txt", "Pages 92-95",
     "I want you to build me agent for opensource contribution PR analyser and person who verifies if"),
    (c5, "You are a senior open-source contributor, pull request strategist, and repository triage analyst.",
     "P043_opensource_pr_analyst_prompt.txt", "Pages 95-99",
     "You are a senior open-source bug hunter, full-stack debugger, and PR-quality analyst."),
    (c5, "You are a senior open-source bug hunter, full-stack debugger, and PR-quality analyst.",
     "P043b_bug_hunter_agent_prompt.txt", "Pages 100-103",
     "Give me an agent prompt to write me a report for an event. It should use report lab python library"),
    
    # P045: NO AGENT PROMPT
    # P047-P051
    (c6, "You are a senior appliance buying analyst, consumer-tech researcher, and decision strategist.",
     "P047_fridge_buying_analyst_prompt.txt", "Pages 105-109",
     "give me an agent prompt who is an expert in cloudflare tunneling an auth managements between"),
    (c6, "You are a senior cloud infrastructure architect, security engineer, and containerized self-hosting specialist.",
     "P049_cloud_infrastructure_architect_prompt.txt", "Pages 109-115",
     "I want an agent prompt to write me these programs in python with outputs extracted and then put"),
    (c6_7, "You are a senior academic programming assistant, Python automation engineer, and PDF report production specialist.",
     "P051_lab_report_production_prompt.txt", "Pages 116-120",
     "i want an agent to investigate a bug I have a project with lightRAG implementation and the bug is"),
    
    # Batch 8: chunk 7
    (c6_7, "You are a senior AI systems engineer, GPU performance analyst, LightRAG specialist, Ollama runtime expert, and root-cause debugging investigator.",
     "P053_gpu_performance_analyst_prompt.txt", "Pages 121-127",
     "I want an agent prompt to remove authentik from my Self hosting setup and just use clouldflare"),
    (c7, "You are a senior self-hosting architect, Cloudflare Zero Trust specialist, security engineer, and infrastructure migration expert.",
     "P055_self_hosting_migration_architect_prompt.txt", "Pages 127-133",
     "I want an agent for setting up this is my self hosted enviroment give me a good prompt for an"),
    (c7, "You are a senior self-hosting architect, media server planner, Docker deployment engineer, and streaming-quality optimization specialist.",
     "P057_media_server_planner_prompt.txt", "Pages 135-140",
     "Give me an agent for this"),
    (c7_8, "You are a senior Servarr ecosystem expert, download automation engineer, self-hosting specialist, and root-cause debugging investigator.",
     "P059_servarr_download_debugger_prompt.txt", "Pages 140-146",
     "Give me a prompt for an agent to create content for a linkedin post based on my repo."),
    
    # Batch 8: chunk 8
    (c8, "You are a senior technical content strategist, LinkedIn ghostwriter, and open-source storytelling specialist.",
     "P061_linkedin_content_strategist_prompt.txt", "Pages 146-148",
     "My PC storage is being filled out I need you to give me an agent that will help me clear out stuff"),
    (c8, "You are a Senior Linux Storage Recovery Engineer, Ubuntu Systems Administrator, and Safe Disk Cleanup Specialist.",
     "P063_storage_recovery_engineer_prompt.txt", "Pages 148-155",
     "I want an agent to write readme files in a professional OS repository way with images in readme"),
    (c8, "You are a senior open-source documentation architect, technical writer, repository maintainer, and visual docs production specialist.",
     "P065_documentation_architect_prompt.txt", "Pages 156-160",
     "Give me a prompt for an agent who is an extremely insane chess genius a person who knows"),
    
    # P066b: NO AGENT PROMPT (chess genius - conversational only)
    
    # Batch 9: chunk 9
    (c9, "You are an expert resume strategist, ATS optimization specialist, Upwork profile writer, and career positioning advisor.",
     "P068_resume_strategist_prompt.txt", "Pages 161-166",
     "Give me a prompt for an agent who has access to information about a full project and they have to"),
    (c9, "You are a senior software architect, implementation planner, and integration testing lead with strong experience in building reliable production systems.",
     "P070_software_architect_phased_build_prompt.txt", "Pages 166-170",
     "Give me an agent prompt  plan implementer and comes up with a plan for implementation after"),  # note: double space in raw text
    
    # P071: no assistant (two user messages in a row)
    # P072 + P073
    (c9, "You are a senior UI/UX engineer, product experience auditor, and front-end usability reviewer.",
     "P073_ui_ux_auditor_prompt.txt", "Pages 171-176",
     "I have this project and architecture but I want an agent to do a deep security and functionality"),
    (c9_10, "You are a principal software auditor, multi-agent systems verifier, security reviewer, reliability engineer, and prompt/tooling specialist.",
     "P075_principal_security_auditor_prompt.txt", "Pages 177-182",
     "For the same project I want you to give me an agent prompt for a UI UX engineer agent."),
    
    # Batch 9-10: chunk 9-10
    (c10, "You are a senior UI/UX engineer, product experience auditor, responsive web design specialist, and front-end usability strategist.",
     "P077_ui_ux_engineer_v2_prompt.txt", "Pages 183-189",
     "I want you to build me an agent prompt for an agent who will not do side fluff or tries to please"),
]

print("=" * 60)
print("Extracting remaining assistant prompts")
print("=" * 60)

extracted = 0
skipped = 0
missing = 0

for chunk, anchor, fname, pages, end_marker in pairs:
    outpath = f"{OUT}/assistant/{fname}"
    if skip_existing and os.path.exists(outpath):
        print(f"  EXISTS: {fname}")
        skipped += 1
        continue
    
    print(f"\n{fname}")
    if extract(chunk, anchor, fname, pages, end_marker):
        extracted += 1
    else:
        missing += 1

# Handle special cases
print("\n=== Special cases ===")

# P045: Cultural report - no "You are" anchor
p045_path = f"{OUT}/assistant/P045_cultural_report_producer_prompt.txt"
if not os.path.exists(p045_path):
    mark_no_prompt("P045_cultural_report_producer_prompt.txt", "Page 104",
                   "Assistant gave conversational advice about PDF report generation but did not produce a structured 'You are' agent prompt.")

# P066b: Chess genius - no "You are" anchor
p066b_path = f"{OUT}/assistant/P066b_chess_genius_agent_prompt.txt"
if not os.path.exists(p066b_path):
    mark_no_prompt("P066b_chess_genius_agent_prompt.txt", "Pages 160-161",
                   "Assistant gave conversational advice about chess coaching but did not produce a structured 'You are' agent prompt. User changed topic to resume before prompt was generated.")

# P071: No assistant prompt (two consecutive user messages)
p071_path = f"{OUT}/assistant/P071_plan_implementer_prompt.txt"
if not os.path.exists(p071_path):
    mark_no_prompt("P071_plan_implementer_prompt.txt", "Pages 170-171",
                   "User sent two consecutive requests (P071 plan implementer, P072 UI/UX audit). No assistant prompt was generated for P071.")

print(f"\nDone! Extracted: {extracted}, Skipped: {skipped}, Missing anchors: {missing}")
print("Special no-prompt cases: P045, P066b, P071")
