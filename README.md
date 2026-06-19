# Prompt Library

A curated collection of system prompts extracted from ChatGPT conversations, organized for easy discovery and reuse.

## Structure

```
prompts/
├── agents/         # Assistant-generated agent system prompts (40 prompts)
├── requests/       # Original user requests that prompted each agent (41 prompts)
└── framework/      # Thinking frameworks and meta-prompts

catalog/
└── INDEX.md        # Master human-readable index with cross-references
```

## Quick Start

| Want... | Go to... |
|---------|----------|
| Browse all prompts | `catalog/INDEX.md` |
| Agent system prompts | `prompts/agents/` |
| Original user requests | `prompts/requests/` |
| Thinking frameworks | `prompts/framework/` |

## Naming Convention

Files follow the pattern: `{P###}-{descriptive-slug}.md`

- `P###` — Unique prompt ID, traceable to the original extraction manifest
- `descriptive-slug` — Human-readable description of the prompt's purpose

## Prompt Categories

- **agents/** — System prompts designed for AI agents to adopt a specific role
- **requests/** — The original user messages that led to each agent prompt
- **framework/** — Meta-prompts for thinking, ideation, and reasoning frameworks
