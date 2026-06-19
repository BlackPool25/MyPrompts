#!/usr/bin/env python3
"""Update the extraction manifest with current state."""

import json, os, glob

MANIFEST = "/home/lightdesk/MyPrompts/extracted_prompts/manifests/extraction_manifest.json"
USER_DIR = "/home/lightdesk/MyPrompts/extracted_prompts/prompts/user"
ASST_DIR = "/home/lightdesk/MyPrompts/extracted_prompts/prompts/assistant"

with open(MANIFEST) as f:
    manifest = json.load(f)

prompts = manifest["prompts"]

# Add missing entries
additions = {
    "P043b": {
        "id": "P043b",
        "type": "assistant",
        "title": "Open-Source Bug Hunter / PR Investigator Agent Prompt",
        "pages": "100-103",
        "topic": "Bug Fixing / Debugging",
        "use_case": "Open-Source Bug Hunting / Feature Debugging",
        "agent_type": "Open-Source Bug Hunter"
    },
    "P045": {
        "id": "P045",
        "type": "assistant",
        "title": "PDF Report Production Agent (Conversational Only — No Prompt)",
        "pages": "104",
        "topic": "Academic / Document Generation",
        "use_case": "Cultural Report PDF Generation (No Prompt)",
        "agent_type": "N/A (No Agent Prompt Generated)"
    },
    "P066b": {
        "id": "P066b",
        "type": "assistant",
        "title": "Chess Genius Agent (Conversational Only — No Prompt)",
        "pages": "160-161",
        "topic": "Education / Chess",
        "use_case": "Chess Coaching Agent Design (No Prompt)",
        "agent_type": "N/A (No Agent Prompt Generated)"
    },
    # Note: P071 remains as "user" type — it's a user request that was followed
    # by another user request (P072). No assistant prompt was generated.
}

for pid, info in additions.items():
    prompts[pid] = info  # Override even if exists (e.g. P071 was user, now assistant placeholder)

# Update totals
user_count = len([p for p in prompts.values() if p["type"] == "user"])
asst_count = len([p for p in prompts.values() if p["type"] == "assistant"])

manifest["total_prompts_identified"] = user_count + asst_count
manifest["prompts_by_type"]["user_prompts"] = user_count
manifest["prompts_by_type"]["assistant_generated_prompts"] = asst_count

# Collect unique topics and agent types (preserving order)
seen_topics = []
for p in prompts.values():
    t = p["topic"]
    if t not in seen_topics:
        seen_topics.append(t)
manifest["topics"] = seen_topics

seen_agents = []
for p in prompts.values():
    a = p["agent_type"]
    if a not in seen_agents:
        seen_agents.append(a)
manifest["agent_types"] = seen_agents

# Write updated manifest
with open(MANIFEST, "w") as f:
    json.dump(manifest, f, indent=2)

print(f"Manifest updated: {user_count} user + {asst_count} assistant = {user_count + asst_count} total")
print(f"Topics: {len(seen_topics)}, Agent types: {len(seen_agents)}")
