#!/usr/bin/env python3
"""
Batch bilingual translation for LLM Wiki pages.
Translates English paragraphs and injects <div class="zh-trans"> after each.
Uses ZhipuAI Anthropic-compatible API.
"""

import os
import re
import json
import urllib.request
import urllib.error
import time
from pathlib import Path

# ── Config ───────────────────────────────────────────────────────────────────
API_KEY = "e2335f9c03da4086bc987f72e0e30b72.PePnGp91BZTUlLPF"
API_URL = "https://open.bigmodel.cn/api/anthropic/v1/messages"
MODEL   = "GLM-5"
CONTENT_DIR = Path("/Users/jimqiu/Downloads/ClaudeCode/LLMWiki/wiki/content/ai-agent-architecture")

# Patterns to skip (frontmatter, wikilinks-only lines, code blocks, empty)
SKIP_PATTERNS = [
    r"^---",           # frontmatter delimiters
    r"^#",             # headings
    r"^\s*$",          # empty lines
    r"^\s*[-*]\s+\[\[", # wikilink-only list items
    r"^\s*[-*]\s+$",   # empty list items
    r"^```",           # code fences
    r"^!\[",           # images
    r"^<div",          # already-inserted zh-trans divs
]

def should_skip(line: str) -> bool:
    return any(re.match(p, line) for p in SKIP_PATTERNS)

def translate_paragraph(text: str) -> str | None:
    """Call ZhipuAI to translate a paragraph. Returns None on failure."""
    payload = json.dumps({
        "model": MODEL,
        "max_tokens": 1024,
        "messages": [{
            "role": "user",
            "content": (
                "请将以下英文翻译成中文，保持专业术语准确，只输出译文，不要任何解释或前缀：\n\n"
                + text
            )
        }]
    }).encode()

    req = urllib.request.Request(
        API_URL,
        data=payload,
        headers={
            "x-api-key": API_KEY,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
        method="POST"
    )

    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read())
                return data["content"][0]["text"].strip()
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(2 ** attempt)
                continue
            print(f"    HTTP {e.code}: {e.read()[:200]}")
            return None
        except Exception as e:
            print(f"    Error: {e}")
            return None
    return None

def process_file(path: Path) -> int:
    """Add zh-trans divs to a markdown file. Returns count of translations added."""
    text = path.read_text(encoding="utf-8")

    # Skip if already has zh-trans (already translated)
    if '<div class="zh-trans">' in text:
        print(f"  SKIP (already translated): {path.name}")
        return 0

    lines = text.split("\n")
    new_lines = []
    in_frontmatter = False
    in_code_block = False
    translations_added = 0

    i = 0
    while i < len(lines):
        line = lines[i]

        # Track frontmatter
        if line.strip() == "---":
            in_frontmatter = not in_frontmatter
            new_lines.append(line)
            i += 1
            continue

        if in_frontmatter:
            new_lines.append(line)
            i += 1
            continue

        # Track code blocks
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
            new_lines.append(line)
            i += 1
            continue

        if in_code_block:
            new_lines.append(line)
            i += 1
            continue

        # Collect a paragraph (consecutive non-empty, non-special lines)
        if line.strip() and not should_skip(line):
            para_lines = [line]
            j = i + 1
            while j < len(lines) and lines[j].strip() and not should_skip(lines[j]):
                para_lines.append(lines[j])
                j += 1

            paragraph = " ".join(para_lines)
            # Only translate if it has actual English content (>20 chars, has letters)
            if len(paragraph) > 20 and re.search(r'[a-zA-Z]{3,}', paragraph):
                zh = translate_paragraph(paragraph)
                if zh:
                    new_lines.extend(para_lines)
                    new_lines.append(f'<div class="zh-trans">{zh}</div>')
                    new_lines.append("")
                    translations_added += 1
                    i = j
                    continue
                else:
                    new_lines.extend(para_lines)
                    i = j
                    continue
            else:
                new_lines.append(line)
                i += 1
                continue
        else:
            new_lines.append(line)
            i += 1

    if translations_added > 0:
        path.write_text("\n".join(new_lines), encoding="utf-8")

    return translations_added

def main():
    md_files = sorted(CONTENT_DIR.rglob("*.md"))
    print(f"Found {len(md_files)} markdown files\n")

    total = 0
    for path in md_files:
        rel = path.relative_to(CONTENT_DIR)
        print(f"Processing: {rel}")
        count = process_file(path)
        if count:
            print(f"  ✓ Added {count} translations")
        total += count
        time.sleep(0.3)  # gentle rate limiting

    print(f"\nDone. Total translations added: {total}")

if __name__ == "__main__":
    main()
