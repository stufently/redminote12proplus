#!/usr/bin/env python3
"""Ask Claude Code for advice using workflow plan/progress files."""

from __future__ import annotations

import argparse
import datetime as dt
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple


DEFAULT_FILES: List[Tuple[str, str]] = [
    ("BACKLOG", "workflow/BACKLOG.md"),
    ("CURRENT_STATE", "workflow/CURRENT_STATE.md"),
    ("SESSION_LOG", "workflow/SESSION_LOG.md"),
    ("HANDOFF", "workflow/HANDOFF.md"),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Collect workflow context and ask Claude Code for prioritized advice."
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        help="Repository root path. Defaults to git root or current directory.",
    )
    parser.add_argument(
        "--focus",
        default="",
        help="Optional focus area that Claude should prioritize.",
    )
    parser.add_argument(
        "--model",
        default="",
        help="Optional Claude model alias/name passed to CLI (for example: sonnet).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Output markdown path. Defaults to workflow/advice/claude-advice-<timestamp>.md",
    )
    parser.add_argument(
        "--stdout-only",
        action="store_true",
        help="Print advice to stdout only and do not write output file.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print generated prompt and exit without calling Claude.",
    )
    parser.add_argument(
        "--max-chars-per-file",
        type=int,
        default=12000,
        help="Maximum characters loaded from each workflow file.",
    )
    parser.add_argument(
        "--language",
        choices=["ru", "en"],
        default="ru",
        help="Preferred response language for Claude.",
    )
    return parser.parse_args()


def resolve_repo_root(user_root: Optional[Path]) -> Path:
    if user_root:
        return user_root.resolve()
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            check=True,
            capture_output=True,
            text=True,
        )
        return Path(result.stdout.strip()).resolve()
    except Exception:
        return Path.cwd().resolve()


def read_file(path: Path, max_chars: int) -> str:
    if not path.exists():
        return "[MISSING FILE]"
    text = path.read_text(encoding="utf-8")
    if len(text) <= max_chars:
        return text
    clipped = text[:max_chars]
    return f"{clipped}\n\n[TRUNCATED: showing first {max_chars} chars]"


def extract_section(markdown: str, heading_names: List[str]) -> List[str]:
    if not markdown or markdown.startswith("[MISSING FILE]"):
        return []
    lines = markdown.splitlines()
    output: List[str] = []
    capture = False
    heading_pattern = re.compile(r"^##\s+(.+?)\s*$")
    targets = {name.lower() for name in heading_names}

    for line in lines:
        match = heading_pattern.match(line)
        if match:
            current = match.group(1).strip().lower()
            capture = current in targets
            continue
        if capture:
            if line.startswith("## "):
                break
            if line.strip().startswith("-"):
                output.append(line.strip())
    return output


def summarize_backlog(markdown: str) -> Dict[str, int]:
    counts: Dict[str, int] = {"todo": 0, "in_progress": 0, "done": 0, "blocked": 0, "other": 0}
    if not markdown or markdown.startswith("[MISSING FILE]"):
        return counts

    for raw in markdown.splitlines():
        line = raw.strip()
        if not line.startswith("|"):
            continue
        parts = [p.strip().lower() for p in line.split("|")]
        if len(parts) < 5:
            continue
        status = parts[3] if parts[1] != "id" else ""
        if status in counts:
            counts[status] += 1
        elif status and status != "---":
            counts["other"] += 1
    return counts


def build_prompt(
    repo_root: Path,
    contents: Dict[str, str],
    focus: str,
    language: str,
) -> str:
    backlog_counts = summarize_backlog(contents.get("BACKLOG", ""))
    done_items = extract_section(contents.get("CURRENT_STATE", ""), ["Готово", "Done"])
    in_progress_items = extract_section(
        contents.get("CURRENT_STATE", ""), ["В работе", "In progress"]
    )
    blocker_items = extract_section(contents.get("CURRENT_STATE", ""), ["Блокеры", "Blockers"])

    lang_line = (
        "Отвечай по-русски. Keep technical terms in English where helpful."
        if language == "ru"
        else "Respond in English."
    )

    focus_line = f"Priority focus: {focus}" if focus else "Priority focus: none"

    return f"""You are acting as an external planning advisor for this repository.
{lang_line}

Goal:
- Review the project plan and execution state.
- Give concrete recommendations for next actions.
- Use completed tasks to infer momentum and suggest realistic scope.

Repository root:
- {repo_root}

Auto summary:
- Backlog counts: todo={backlog_counts['todo']}, in_progress={backlog_counts['in_progress']}, done={backlog_counts['done']}, blocked={backlog_counts['blocked']}, other={backlog_counts['other']}
- CURRENT_STATE done items: {len(done_items)}
- CURRENT_STATE in-progress items: {len(in_progress_items)}
- CURRENT_STATE blockers: {len(blocker_items)}
- {focus_line}

Required output format:
1) Executive assessment (4-8 bullet points)
2) Risks and blind spots (up to 5 bullets)
3) Priority next actions (numbered list, exactly 5 items, each item must reference a concrete file to update)
4) Backlog updates (which items to add/remove/re-prioritize)
5) Definition of done for the next session (short checklist)

Context files:

### BACKLOG (workflow/BACKLOG.md)
```md
{contents.get("BACKLOG", "[MISSING FILE]")}
```

### CURRENT_STATE (workflow/CURRENT_STATE.md)
```md
{contents.get("CURRENT_STATE", "[MISSING FILE]")}
```

### SESSION_LOG (workflow/SESSION_LOG.md)
```md
{contents.get("SESSION_LOG", "[MISSING FILE]")}
```

### HANDOFF (workflow/HANDOFF.md)
```md
{contents.get("HANDOFF", "[MISSING FILE]")}
```
"""


def run_claude(prompt: str, model: str) -> str:
    cmd = ["claude", "-p", "--output-format", "text", prompt]
    if model:
        cmd = ["claude", "-p", "--output-format", "text", "--model", model, prompt]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        stderr = result.stderr.strip()
        raise RuntimeError(f"Claude CLI failed with code {result.returncode}: {stderr}")
    return result.stdout.strip()


def default_output_path(repo_root: Path) -> Path:
    ts = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    return repo_root / "workflow" / "advice" / f"claude-advice-{ts}.md"


def write_output(path: Path, model: str, focus: str, advice: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    timestamp = dt.datetime.now().isoformat(timespec="seconds")
    header = [
        "# Claude Advice",
        "",
        f"- Timestamp: {timestamp}",
        f"- Model: {model or 'default'}",
        f"- Focus: {focus or 'none'}",
        "",
        "## Response",
        "",
    ]
    path.write_text("\n".join(header) + advice.strip() + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    repo_root = resolve_repo_root(args.repo_root)

    contents: Dict[str, str] = {}
    for key, rel in DEFAULT_FILES:
        path = repo_root / rel
        contents[key] = read_file(path, args.max_chars_per_file)

    prompt = build_prompt(repo_root, contents, args.focus.strip(), args.language)

    if args.dry_run:
        print(prompt)
        return 0

    try:
        advice = run_claude(prompt, args.model.strip())
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    if args.stdout_only:
        print(advice)
        return 0

    output_path = args.output.resolve() if args.output else default_output_path(repo_root)
    write_output(output_path, args.model.strip(), args.focus.strip(), advice)
    print(f"Saved advice to: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
