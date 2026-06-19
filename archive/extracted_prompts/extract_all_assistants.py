#!/usr/bin/env python3
"""
Extract all remaining assistant prompts by:
1. Reading each existing user file's first content line
2. Finding it in the raw text chunks
3. Extracting the assistant "You are" anchor that follows
4. Cutting at the next user anchor or "Show moreShow less"
"""

import os, re, glob

RAW_DIR = "/home/lightdesk/MyPrompts/extracted_prompts"
OUT = f"{RAW_DIR}/prompts"

def strip_pages(t):
    t = re.sub(r"Printed using ChatGPT to PDF, powered by PDFCrowd HTML to PDF API\. \d+/190", "", t)
    t = re.sub(r"=+\nPAGE \d+\n=+", "", t)
    return t

def clean(text):
    return strip_pages(text).strip()

def get_user_first_line(user_fname):
    """Get the first actual content line from a user prompt file (after header)."""
    with open(f"{OUT}/user/{user_fname}") as f:
        lines = f.readlines()
    for line in lines:
        line = line.strip()
        if line and not line.startswith("SOURCE:") and not line.startswith("TYPE:") and not line.startswith("==="):
            return line
    return None

def find_in_chunks(text, chunks):
    """Search for text in concatenated chunks, return (chunk_idx, position)."""
    for i, (name, content) in enumerate(chunks):
        pos = content.find(text)
        if pos >= 0:
            return i, pos
    return None, None

def extract_assistant_after_user(user_anchor, chunks, output_fname, src_pages, next_user_anchor=None):
    """Find the user anchor, then extract the assistant response after it."""
    # Search all chunks
    found = None
    for ci, (cname, ccontent) in enumerate(chunks):
        pos = ccontent.find(user_anchor)
        if pos >= 0:
            found = (ci, pos, ccontent)
            break
    
    if not found:
        print(f"  USER NOT FOUND: {user_anchor[:70]}")
        return False
    
    ci, upos, ccontent = found
    after_user = ccontent[upos + len(user_anchor):]
    
    # Find the "You are" anchor after the user message
    # But first check for "Show moreShow less" which separates user from assistant
    if "Show moreShow less" in after_user:
        after_split = after_user.split("Show moreShow less", 1)[1]
    else:
        after_split = after_user
    
    # Find "You are" anchor in the assistant response
    you_are_match = re.search(r"You are[^.]*\.", after_split)
    if not you_are_match:
        print(f"  NO 'You are' anchor found after user: {user_anchor[:50]}")
        return False
    
    asst_start = you_are_match.start()
    asst_anchor = you_are_match.group()
    asst_text = after_split[asst_start:]
    
    # Cut at next user anchor if provided
    if next_user_anchor:
        nu_pos = asst_text.find(next_user_anchor)
        if nu_pos >= 0:
            asst_text = asst_text[:nu_pos]
    
    # Also try to cut at next "Show moreShow less" if it appears
    if "Show moreShow less" in asst_text:
        # Only cut if the "Show moreShow less" is followed by a user-like pattern
        parts = asst_text.split("Show moreShow less")
        cleaned = clean(parts[0])
        print(f"  Cut at Show more: {len(cleaned)} chars")
        asst_text = parts[0]
    
    result = clean(asst_text)
    
    if len(result) < 50:
        print(f"  WARNING: Very short result ({len(result)} chars) for {output_fname}")
    
    with open(f"{OUT}/assistant/{output_fname}", "w") as f:
        f.write(f"SOURCE: Improving Testing Prompt.pdf, {src_pages}\nTYPE: Assistant-Generated Agent Prompt (VERBATIM EXTRACT)\n================================================================================\n\n{result}")
    print(f"  {output_fname}: {len(result)} chars")
    return True

# Load all raw text chunks
chunk_files = sorted(glob.glob(f"{RAW_DIR}/raw_text_*.txt"))
chunks = []
for f in chunk_files:
    name = os.path.basename(f)
    with open(f) as fh:
        chunks.append((name, fh.read()))

# ========== MAPPING: user file -> (assistant file, pages, next user file for end marker) ==========

pairs = [
    # Batch 6 leftovers
    ("P022_database_recovery_supabase_request.txt", "P023_database_recovery_agent_prompt.txt", "Pages 49-54", "P024_policysattva_e2e_testing_request.txt"),
    ("P024_policysattva_e2e_testing_request.txt", "P025_policysattva_qa_agent_prompt.txt", "Pages 56-60", "P026_frontend_refactor_docker_request.txt"),
    ("P026_frontend_refactor_docker_request.txt", "P027_frontend_architect_refactor_prompt.txt", "Pages 61-66", "P028_hero_image_generation_request.txt"),
    ("P028_hero_image_generation_request.txt", "P029_visual_designer_hero_image_prompt.txt", "Pages 67-70", "P030_slow_indexing_investigation_request.txt"),
    ("P030_slow_indexing_investigation_request.txt", "P031_rag_performance_debugger_prompt.txt", "Pages 70-74", "P032_internship_project_evaluation_request.txt"),
    ("P032_internship_project_evaluation_request.txt", "P033_backend_project_strategist_prompt.txt", "Pages 75-81", "P034_academic_report_creator_request.txt"),

    # Batch 7: chunks 5-6
    ("P034_academic_report_creator_request.txt", "P035_academic_report_creator_prompt.txt", "Pages 81-84", "P036_leetcode_report_request.txt"),
    ("P036_leetcode_report_request.txt", "P037_leetcode_report_agent_prompt.txt", "Pages 85-87", "P038_teaching_agent_design_request.txt"),
    ("P038_teaching_agent_design_request.txt", "P039_learning_coach_tutor_prompt.txt", "Pages 88-92", "P040_qwen_llama_cpp_debug_request.txt"),
    ("P040_qwen_llama_cpp_debug_request.txt", "P041_llm_runtime_debug_engineer_prompt.txt", "Pages 92-95", "P042_opensource_pr_analyzer_request.txt"),
    ("P042_opensource_pr_analyzer_request.txt", "P043_opensource_pr_analyst_prompt.txt", "Pages 95-99", "P044_cultural_report_with_reportlab_request.txt"),

    # Hidden pair: pages 100-103 (BUG HUNTER - not in manifest)
    ("P044_cultural_report_with_reportlab_request.txt", "P043b_bug_hunter_agent_prompt.txt", "Pages 100-103", "P046_fridge_buying_agent_request.txt"),
    # BUT: the pair before P044 needs special handling - it starts from a user embedded after P043

    # The P045 doesn't have a "You are" anchor - it's conversational only
    # Skip to P047

    ("P046_fridge_buying_agent_request.txt", "P047_fridge_buying_analyst_prompt.txt", "Pages 105-109", "P048_cloudflare_infrastructure_expert_request.txt"),
    ("P048_cloudflare_infrastructure_expert_request.txt", "P049_cloud_infrastructure_architect_prompt.txt", "Pages 109-115", "P050_lab_report_with_reportlab_request.txt"),
    ("P050_lab_report_with_reportlab_request.txt", "P051_lab_report_production_prompt.txt", "Pages 116-120", "P052_gpu_usage_bug_investigation_request.txt"),

    # Batch 8: chunks 7-8
    ("P052_gpu_usage_bug_investigation_request.txt", "P053_gpu_performance_analyst_prompt.txt", "Pages 121-127", "P054_remove_authentik_migration_request.txt"),
    ("P054_remove_authentik_migration_request.txt", "P055_self_hosting_migration_architect_prompt.txt", "Pages 127-133", "P056_media_server_setup_request.txt"),
    ("P056_media_server_setup_request.txt", "P057_media_server_planner_prompt.txt", "Pages 135-140", "P058_sonarr_qbittorrent_stopped_request.txt"),
    ("P058_sonarr_qbittorrent_stopped_request.txt", "P059_servarr_download_debugger_prompt.txt", "Pages 140-146", "P060_linkedin_post_creator_request.txt"),
    ("P060_linkedin_post_creator_request.txt", "P061_linkedin_content_strategist_prompt.txt", "Pages 146-148", "P062_ubuntu_storage_cleanup_request.txt"),
    ("P062_ubuntu_storage_cleanup_request.txt", "P063_storage_recovery_engineer_prompt.txt", "Pages 148-155", "P064_readme_docs_writing_request.txt"),
    ("P064_readme_docs_writing_request.txt", "P065_documentation_architect_prompt.txt", "Pages 156-160", "P066_chess_genius_agent_request.txt"),

    # Batch 9: chunks 8-9
    ("P066_chess_genius_agent_request.txt", "P066b_chess_genius_agent_prompt.txt", "Pages 160-161", "P067_resume_builder_request.txt"),
    ("P067_resume_builder_request.txt", "P068_resume_strategist_prompt.txt", "Pages 161-166", "P069_phased_build_plan_agent_request.txt"),
    ("P069_phased_build_plan_agent_request.txt", "P070_software_architect_phased_build_prompt.txt", "Pages 166-170", "P071_plan_implementer_with_context7_request.txt"),
    # P071 + P072 are BOTH user messages (plan implementer + UI/UX audit)
    ("P072_ui_ux_audit_agent_request.txt", "P073_ui_ux_auditor_prompt.txt", "Pages 171-176", "P074_deep_security_audit_request.txt"),
    ("P074_deep_security_audit_request.txt", "P075_principal_security_auditor_prompt.txt", "Pages 177-182", "P076_ui_ux_engineer_v2_request.txt"),
    ("P076_ui_ux_engineer_v2_request.txt", "P077_ui_ux_engineer_v2_prompt.txt", "Pages 183-189", "P078_brainstorming_ideation_agent_request.txt"),
]

# The P071 followed by P072 are both user prompts. P071 is answered as assistant
# before P072. Let me handle this:
# P070 assistant ends at P071 user. P071 user → ??? assistant → P072 user
# There's no assistant prompt for P071 in the manifest!
# The flow seems to be: P071 user → P072 user (two consecutive user messages),
# then P073 assistant responds to P072

# Special: P071 has NO assistant (user message only, then another user)
# Let me remove it from the list

# Actually wait, P071 is "Plan Implementer with Context7 Research". Let me check
# the raw text for what comes between P071 user and P072 user in chunk9.

print("=" * 60)
print("Extracting all remaining assistant prompts")
print("=" * 60)

for user_file, asst_file, pages, next_user_file in pairs:
    # Skip if already exists
    asst_path = f"{OUT}/assistant/{asst_file}"
    if os.path.exists(asst_path):
        print(f"  EXISTS: {asst_file}")
        continue
    
    user_anchor = get_user_first_line(user_file)
    if not user_anchor:
        print(f"  CANNOT READ: {user_file}")
        continue
    
    next_anchor = get_user_first_line(next_user_file) if next_user_file else None
    
    print(f"\n  User: {user_file}")
    print(f"  -> {asst_file}")
    
    # For the hidden bug hunter prompt, use the anchor directly
    if asst_file == "P043b_bug_hunter_agent_prompt.txt":
        # This follows the P043 assistant. The user is embedded in chunk5
        # Use the direct "You are" approach
        for ci, (cname, ccontent) in enumerate(chunks):
            if "You are a senior open-source bug hunter, full-stack debugger, and PR-quality analyst." in ccontent:
                text = ccontent.split("You are a senior open-source bug hunter, full-stack debugger, and PR-quality analyst.", 1)[1]
                text = "You are a senior open-source bug hunter, full-stack debugger, and PR-quality analyst." + text
                if next_anchor and next_anchor in text:
                    text = text.split(next_anchor)[0]
                if "Show moreShow less" in text:
                    text = text.split("Show moreShow less")[0]
                result = clean(text)
                with open(asst_path, "w") as f:
                    f.write(f"SOURCE: Improving Testing Prompt.pdf, {pages}\nTYPE: Assistant-Generated Agent Prompt (VERBATIM EXTRACT)\n================================================================================\n\n{result}")
                print(f"  {asst_file}: {len(result)} chars")
                break
        continue
    
    extract_assistant_after_user(user_anchor, chunks, asst_file, pages, next_anchor)

print("\nDone!")
