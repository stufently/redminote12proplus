---
name: claude-plan-advisor
description: Automatically ask Claude Code for actionable advice based on project planning and progress files. Use when Codex needs external second-opinion guidance on what to do next, how to improve the current plan, how to reassess completed tasks, or how to prioritize backlog items using workflow/BACKLOG.md, workflow/CURRENT_STATE.md, workflow/SESSION_LOG.md, and workflow/HANDOFF.md.
---

# Claude Plan Advisor

## Overview

Use a deterministic script to collect the current project state, send it to Claude Code, and save advice as a timestamped artifact in `workflow/advice/`.

## Run Workflow

1. Confirm that `workflow/` files exist (`BACKLOG.md`, `CURRENT_STATE.md`, `SESSION_LOG.md`, `HANDOFF.md`).
2. Run the advisor script from repository root:

```bash
python3 skills/claude-plan-advisor/scripts/ask_claude_plan_advice.py
```

3. If a specific objective is needed, pass `--focus`:

```bash
python3 skills/claude-plan-advisor/scripts/ask_claude_plan_advice.py \
  --focus "Improve night-photography section quality and reduce duplication"
```

4. Check the saved result in `workflow/advice/claude-advice-*.md`.
5. Apply accepted advice by updating `workflow/BACKLOG.md`, `workflow/CURRENT_STATE.md`, and `workflow/HANDOFF.md`.

## Validate Prompt Without API Call

Use `--dry-run` to preview the exact prompt that will be sent:

```bash
python3 skills/claude-plan-advisor/scripts/ask_claude_plan_advice.py --dry-run
```

## Script Options

- `--focus "<text>"`: add a high-priority focus area
- `--model "<model>"`: forward model override to `claude`
- `--output <path>`: write advice to a custom file path
- `--stdout-only`: print advice only, do not write file
- `--dry-run`: print built prompt and exit
- `--max-chars-per-file N`: cap file content length in prompt (default `12000`)
- `--language ru|en`: set output language preference (default `ru`)

## Resource Map

### scripts/
- `ask_claude_plan_advice.py`: collect workflow context, call Claude CLI, save advice artifact

### references/
- `prompt-contract.md`: expected structure and quality bar for Claude advice
