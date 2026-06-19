# Prompt Library

A curated collection of system prompts extracted from ChatGPT conversations, organized for easy discovery and reuse.

## Structure

```
prompts/
├── agents/         # Assistant-generated agent system prompts (40 prompts)
├── requests/       # Original user requests that prompted each agent (41 prompts)
└── framework/      # Thinking frameworks and meta-prompts

catalog/
├── INDEX.md        # Master human-readable index with cross-references
└── manifest.json   # Machine-readable catalog with metadata

archive/            # Raw extraction artifacts (source PDF, scripts, raw text)
```

## Quick Start

| Want... | Go to... |
|---------|----------|
| Browse all prompts | `catalog/INDEX.md` |
| Agent system prompts | `prompts/agents/` |
| Original user requests | `prompts/requests/` |
| Thinking frameworks | `prompts/framework/` |
| Raw extraction data | `archive/extracted_prompts/` |

## Naming Convention

Files follow the pattern: `{P###}-{descriptive-slug}.md`

- `P###` — Unique prompt ID, traceable to the original extraction manifest
- `descriptive-slug` — Human-readable description of the prompt's purpose

## Prompt Categories

- **agents/** — System prompts designed for AI agents to adopt a specific role
- **requests/** — The original user messages that led to each agent prompt
- **framework/** — Meta-prompts for thinking, ideation, and reasoning frameworks

## Archive

The `archive/` directory preserves all original extraction materials:

- `extracted_prompts/` — Original extraction artifacts (scripts, raw text, manifests)
- `Improving Testing Prompt.pdf` — Source PDF (190-page ChatGPT conversation export)

## Source

All prompts were extracted from the ChatGPT conversation export `Improving Testing Prompt.pdf` (190 pages, 80 identified prompts) using pypdf-based text extraction.
