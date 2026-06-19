#!/usr/bin/env python3
"""Build index files from the manifest and prompt file inventory."""

import json, os

MANIFEST = "/home/lightdesk/MyPrompts/extracted_prompts/manifests/extraction_manifest.json"
INDEX_DIR = "/home/lightdesk/MyPrompts/extracted_prompts/index"
PROMPTS_DIR = "/home/lightdesk/MyPrompts/extracted_prompts/prompts"

with open(MANIFEST) as f:
    manifest = json.load(f)

prompts = manifest["prompts"]

# Build reverse maps
topic_map = {}
use_case_map = {}
agent_map = {}

for pid, info in prompts.items():
    topic = info.get("topic", "Unknown")
    use_case = info.get("use_case", "Unknown")
    agent = info.get("agent_type", "N/A")
    
    topic_map.setdefault(topic, []).append(pid)
    use_case_map.setdefault(use_case, []).append(pid)
    agent_map.setdefault(agent, []).append(pid)

# Additional prompts not in manifest (P043b bug hunter, P045 no-prompt, P066b chess, P071 no-prompt)
topic_map.setdefault("Bug Fixing / Debugging", []).append("P043b")
use_case_map.setdefault("Open-Source Bug Hunting / Feature Debugging", []).append("P043b")
agent_map.setdefault("Open-Source Bug Hunter", []).append("P043b")

# Helper: get file path
def prompt_file(pid, ptype):
    if ptype == "N/A (User Request)":
        return None
    udir = f"{PROMPTS_DIR}/assistant"
    for f in os.listdir(udir):
        if f.startswith(pid.replace('P', 'P').replace('b', '') + "_") or f.startswith(pid + "_") or f == f"{pid}_NO_AGENT_PROMPT_GENERATED.txt":
            return f
        if pid == "P043b" and f.startswith("P043b_"):
            return f
    return None

def write_index(dirname, data, title_key, value_key):
    """Write index file for a given categorization."""
    outpath = f"{INDEX_DIR}/{dirname}/README.md"
    with open(outpath, "w") as f:
        f.write(f"# Index by {title_key}\n\n")
        for key in sorted(data.keys()):
            items = data[key]
            f.write(f"## {key}\n\n")
            for pid in sorted(items):
                num_part = pid.replace('P', '').replace('b', '')
                default_type = "user" if int(num_part) % 2 == 1 else "assistant"
                info = prompts.get(pid, {"type": default_type, "title": "", "pages": ""})
                ptype = info.get("type", "?")
                pfile = prompt_file(pid, info.get("agent_type", "N/A"))
                if pfile:
                    f.write(f"- **{pid}** ({ptype}): {info.get('title', '')} — `assistant/{pfile}`\n")
                else:
                    f.write(f"- **{pid}** ({ptype}): {info.get('title', '')} — (user request, no agent prompt)\n")
            f.write("\n")
    print(f"  Wrote {outpath} ({len(data)} categories)")

# Write indexes
write_index("by-topic", topic_map, "Topic", "prompts")
write_index("by-use-case", use_case_map, "Use Case", "prompts")
write_index("by-agent-type", agent_map, "Agent Type", "prompts")

print("Done building indexes")
