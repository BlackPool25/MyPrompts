#!/usr/bin/env python3
"""Batch 6: Extract P022-P033 from raw_text_41_60.txt and raw_text_61_80.txt"""

import os, re

RAW_DIR = "/home/lightdesk/MyPrompts/extracted_prompts"
OUT = f"{RAW_DIR}/prompts"

def strip_pages(t):
    return re.sub(r"\n?Printed using ChatGPT to PDF, powered by PDFCrowd HTML to PDF API\. \d+/190\n?", "", t)

def extract_pair(text, user_anchor, asst_anchor, user_fname, asst_fname, user_src, asst_src, end_marker=None):
    if user_anchor not in text:
        print(f"  MISSING user: {user_anchor[:40]}")
        return
    after_user = text.split(user_anchor, 1)[1]
    user_text = user_anchor + after_user
    
    if "Show moreShow less" in user_text:
        user_only = user_text.split("Show moreShow less")[0]
    else:
        user_only = user_text
    
    user_only = strip_pages(user_only).strip()
    
    with open(f"{OUT}/user/{user_fname}", "w") as f:
        f.write(f"SOURCE: Improving Testing Prompt.pdf, {user_src}\nTYPE: User Prompt (VERBATIM EXTRACT)\n================================================================================\n\n{user_only}")
    print(f"  {user_fname}: {len(user_only)} chars")
    
    if asst_anchor and asst_anchor in text:
        asst_text = text.split(asst_anchor, 1)[1]
        if end_marker and end_marker in asst_text:
            asst_text = asst_text.split(end_marker)[0]
        asst_full = asst_anchor + asst_text
        asst_full = strip_pages(asst_full).strip()
        with open(f"{OUT}/assistant/{asst_fname}", "w") as f:
            f.write(f"SOURCE: Improving Testing Prompt.pdf, {asst_src}\nTYPE: Assistant-Generated Agent Prompt (VERBATIM EXTRACT)\n================================================================================\n\n{asst_full}")
        print(f"  {asst_fname}: {len(asst_full)} chars")

txt41 = open(f"{RAW_DIR}/raw_text_41_60.txt").read()
txt61 = open(f"{RAW_DIR}/raw_text_61_80.txt").read()

# P022+P023: Database recovery
print("=== P022+P023 ===")
extract_pair(txt41,
    "I want you to give me an agent prompt for a specific use case",
    "You are a senior database recovery, reverse-engineering, and Supabase/Postgres architecture agent.",
    "P022_database_recovery_supabase_request.txt",
    "P023_database_recovery_agent_prompt.txt",
    "Page 49", "Pages 49-54",
    end_marker="I need an agent to test this Project end to end")

# P024+P025: PolicySattva E2E testing
print("=== P024+P025 ===")
extract_pair(txt41,
    "I need an agent to test this Project end to end",
    "You are a senior full-stack QA, debugging, and data-repair agent for the PolicySattva project.",
    "P024_policysattva_e2e_testing_request.txt",
    "P025_policysattva_qa_agent_prompt.txt",
    "Pages 54-55", "Pages 56-60",
    end_marker="Give me an agent prompt who will fix this up")

# P026+P027: Frontend refactor
print("=== P026+P027 ===")
extract_pair(txt61,
    "Give me an agent prompt who will fix this up and refactor the frontend",
    "You are a senior frontend architect, full-stack integration engineer, and product-quality implementation agent for PolicySattva.",
    "P026_frontend_refactor_docker_request.txt",
    "P027_frontend_architect_refactor_prompt.txt",
    "Pages 60-61", "Pages 61-66",
    end_marker="I want an agent to create me a background image")

# P028+P029: Hero image generation
print("=== P028+P029 ===")
extract_pair(txt61,
    "I want an agent to create me a background image to use in my hero section",
    "You are a world-class visual designer and generative art director creating a hero-section background image",
    "P028_hero_image_generation_request.txt",
    "P029_visual_designer_hero_image_prompt.txt",
    "Page 67", "Pages 67-70",
    end_marker="Give me an agent to fix this issue")

# P030+P031: Indexing performance
print("=== P030+P031 ===")
extract_pair(txt61,
    "Give me an agent to fix this issue and also ensure everything is working properly",
    "You are a senior AI systems engineer, RAG architect, and performance debugging specialist for PolicySattva.",
    "P030_slow_indexing_investigation_request.txt",
    "P031_rag_performance_debugger_prompt.txt",
    "Page 70", "Pages 70-74",
    end_marker="So I am trying to get an internship")

# P032+P033: Internship project evaluation
print("=== P032+P033 ===")
extract_pair(txt61,
    "So I am trying to get an internship and trying to learn everything I need to know",
    "You are a senior backend project strategist, Java/Spring architect, and internship-readiness evaluator.",
    "P032_internship_project_evaluation_request.txt",
    "P033_backend_project_strategist_prompt.txt",
    "Pages 74-75", "Pages 75-81",
    end_marker="I want an project report creator agent for this project")

print("Done batch 6")
