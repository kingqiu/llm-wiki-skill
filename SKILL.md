---
name: llm-wiki
version: 0.3.0
description: |
  Build, query, and maintain a personal LLM-powered wiki from a local knowledge base.
  Features three distinct modes: Ingest (add knowledge), Query (ask questions), and Lint (health check).
  Supports multiple knowledge source directories, automatic Quartz initialization, and GitHub Pages sync.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - AskUserQuestion
  - WebSearch
  - WebFetch
  - Skill
  - Agent
---

# /llm-wiki — LLM Wiki Manager

Build and maintain a personal knowledge wiki following the [LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) by Andrej Karpathy.

---

## Phase 0: Startup Check (ALWAYS RUN FIRST)

Before doing anything else, check if the skill has been configured:

```
Read the file: ~/.claude/skills/llm-wiki/config.md
```

- **If the file exists AND `configured: true` is in the frontmatter:** Parse the config and proceed to Phase 1 (Intent Routing). Extract:
  - `SOURCE_DIRS`: list of paths under "## Source Directories"
  - `WIKI_DIR`: path under "## Wiki Directory"
  - `GITHUB_PAGES`: URL under "## GitHub Pages" (may be empty)

- **If the file does not exist OR `configured: true` is missing:** Run the **First-Time Setup Wizard** below before proceeding.

---

## First-Time Setup Wizard

Greet the user and explain this is a one-time setup. Run these three steps in order:

### Setup Step 1: Dependency Check

Run the following checks silently:

```bash
node --version 2>/dev/null
git --version 2>/dev/null
```

- If Node.js is **not found** or version is below v18:
  ```
  ❌ 未检测到 Node.js（v18 或以上）。
  请先安装：https://nodejs.org
  安装完成后，重新运行 /llm-wiki 继续配置。
  ```
  **Stop here.** Do not proceed until the user resolves this.

- If Git is **not found**:
  ```
  ❌ 未检测到 Git。
  请先安装：https://git-scm.com
  安装完成后，重新运行 /llm-wiki 继续配置。
  ```
  **Stop here.**

- If both are found, tell the user: `✅ 环境检查通过（Node.js vX.X.X，Git vX.X.X）`

### Setup Step 2: Knowledge Base Directories

Ask the user:
```
请输入你的知识库目录路径。
支持多个目录，每行输入一个。输入完成后告诉我。

例如：
/Users/yourname/Obsidian/Raw
/Users/yourname/Obsidian/Learning
```

For each path the user provides:
- Verify it exists: `ls "{path}" 2>/dev/null`
- If it does not exist, warn: `⚠️ 路径不存在：{path}，请确认后重新输入`
- Ask user to confirm the final list before saving

### Setup Step 3: Wiki Directory

Ask the user:
```
Wiki 要保存在哪个目录？
如果目录不存在，我会自动帮你初始化一个新的 Quartz 项目。

例如：/Users/yourname/MyWiki
```

After the user provides the path:

**Case A — Directory already exists and contains a Quartz project** (check for `quartz.config.ts`):
```
✅ 检测到已有的 Quartz Wiki 项目，直接使用。
```

**Case B — Directory does not exist or is empty:**
```
📦 正在初始化 Quartz Wiki 项目，请稍候...
```
Run the following to initialize:
```bash
git clone https://github.com/jackyzha0/quartz.git "{WIKI_DIR}"
cd "{WIKI_DIR}"
npm install
```
Then apply the standard wiki configuration:
- Set `pageTitle` to `"LLM Wiki"` in `quartz.config.ts`
- Create `content/index.md` with a basic welcome page
- Create `content/log.md` with initial entry
- Create `SCHEMA.md` (copy the standard schema — see Schema section below)

Tell the user when done: `✅ Quartz Wiki 初始化完成：{WIKI_DIR}`

### Setup Step 4: GitHub Pages (Optional)

Ask the user:
```
（选填）你的 GitHub Pages 地址是什么？
格式如：https://username.github.io/LLMWiki
直接回车跳过。
```

### Save Config

Write the collected values to `~/.claude/skills/llm-wiki/config.md`:

```markdown
---
configured: true
---

# LLM Wiki 配置文件

此文件由 /llm-wiki 首次运行向导自动生成。如需修改，直接编辑对应字段即可。

## Source Directories
# 知识库目录（支持多个路径，每行一个）
- {path1}
- {path2}

## Wiki Directory
{wiki_dir}

## GitHub Pages
{github_pages_url}
```

Tell the user: `✅ 配置已保存！下次运行 /llm-wiki 将直接使用这些设置。`

Then proceed to Phase 1 (Intent Routing).

---

## Phase 1: Intent Routing

Read `{WIKI_DIR}/content/index.md` to understand the current wiki structure, then determine the user's intent from their input:

1. **Asking a question about existing knowledge** → Go to **Query Flow**
2. **Requesting cleanup, health check, or gap finding** → Go to **Lint Flow**
3. **Providing a topic to research or new sources** → Go to **Ingest Flow**

If the intent is ambiguous, ask the user which of the three operations they want to perform.

---

## Ingest Flow (Knowledge Building)

### Step 1: Topic Resolution

Based on the user's input and `index.md`, determine if this is a new topic or relates to an existing one:
- **Clearly a new topic:** Tell the user and prepare to create a new topic directory.
- **Clearly related to an existing topic:** Tell the user "这与已有话题 [Topic Name] 相关，准备补充资料。"
- **Ambiguous:** Present the closest 1-2 existing topics and ask: 新建新话题，还是补充到现有话题中？

### Step 2: Scope Clarification

Ask the user (concisely, max 2 rounds):
1. **Mode:** 批量模式（一次处理完，结束后再看结果）or 精读模式（每个资料处理完暂停确认）?
2. **Focus:** 有没有特别想深入的方向，或偏好的资料类型？

### Step 3: Source Discovery

Scan all `SOURCE_DIRS` for relevant files:
```bash
find "{source_dir}" -type f \( -name "*.md" -o -name "*.pdf" -o -name "*.png" -o -name "*.jpg" -o -name "*.jpeg" -o -name "*.webp" \) 2>/dev/null
```
Run this for each directory in `SOURCE_DIRS`. Merge results, filter by relevance, present to user grouped by type (MD / PDF / Image), and ask for confirmation.

Threshold rules:
- **< 3 files:** Proactively suggest web search for supplementary materials
- **3–9 files:** Offer web search as an option
- **≥ 10 files:** Proceed directly, optionally offer enrichment

### Step 4: Wiki Construction

Read `{WIKI_DIR}/SCHEMA.md` FIRST to strictly follow page format and wikilink rules.

**Batch mode:** Process all sources at once, generate all pages, then show the user a summary.

**Deep-read mode:** Process one source at a time, show the result, wait for feedback, then proceed to the next.

For each source:
1. Generate a source summary page in `{WIKI_DIR}/content/{topic}/sources/`
2. Create or update concept pages in `{WIKI_DIR}/content/{topic}/concepts/`
3. Create or update entity pages in `{WIKI_DIR}/content/{topic}/entities/`
4. Create synthesis pages for cross-cutting insights in `{WIKI_DIR}/content/{topic}/synthesis/`
5. Write or update `{WIKI_DIR}/content/{topic}/overview.md`
6. Update `{WIKI_DIR}/content/index.md`
7. Append to `{WIKI_DIR}/content/log.md` using format: `## [YYYY-MM-DD] ingest | {topic} | {source_title}`

**Wikilink rule (CRITICAL):** Always use full paths from the content root:
- ✅ `[[topic-name/concepts/concept-name|Display Text]]`
- ❌ `[[concepts/concept-name|Display Text]]`

### Step 5: Build & Preview

```bash
cd "{WIKI_DIR}" && npx quartz build
```

Then start the local server:
```bash
cd "{WIKI_DIR}" && python3 serve.py
```

Tell the user: `Wiki 已构建完成，本地预览地址：http://localhost:8888`

If `serve.py` does not exist in the wiki directory, create it first using the standard clean-URL server template.

Offer to sync to GitHub Pages if `GITHUB_PAGES` is configured.

---

## Query Flow (Asking Questions)

1. **Search:** Read `{WIKI_DIR}/content/index.md`, identify relevant pages, read them.
2. **Answer:** Synthesize a comprehensive answer with citations.
3. **Capture insight:** After answering, ALWAYS ask: `这个分析有价值，要作为综合分析（Synthesis）存入 Wiki 吗？`
4. **Save (if yes):** Create a synthesis page in the relevant topic's `synthesis/` directory, update `index.md`, append to `log.md`.

---

## Lint Flow (Wiki Health Check)

1. **Broken links:** Find wikilinks pointing to non-existent pages.
2. **Orphan pages:** Find pages with no inbound links.
3. **Missing concept pages:** Find concepts mentioned in text but lacking their own pages.
4. **Contradictions:** Identify claims that conflict across pages.
5. **Knowledge gaps:** Propose 2-3 specific questions the wiki cannot currently answer — and suggest web searches to fill them.
6. **Report:** Present all findings clearly to the user.
7. **Action:** Offer to (a) auto-fix broken links and orphans, and (b) run a web search to fill the top knowledge gap.

After lint, append to `log.md`: `## [YYYY-MM-DD] lint | {summary of findings}`

---

## Standard serve.py Template

If `{WIKI_DIR}/serve.py` does not exist during Step 5, create it with this content:

```python
import http.server
import os
import sys

DIRECTORY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public")
PORT = 8888

class CleanURLHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_GET(self):
        path = self.path.split("?")[0].split("#")[0]
        full = os.path.join(DIRECTORY, path.lstrip("/"))
        if not os.path.exists(full):
            if os.path.exists(full + ".html"):
                self.path = path + ".html"
            elif os.path.exists(os.path.join(full, "index.html")):
                self.path = path + "/index.html"
            else:
                if os.path.exists(os.path.join(DIRECTORY, "404.html")):
                    self.path = "/404.html"
        super().do_GET()

    def log_message(self, format, *args):
        pass

with http.server.HTTPServer(("", PORT), CleanURLHandler) as httpd:
    print(f"Serving at http://localhost:{PORT}")
    httpd.serve_forever()
```

---

## Important Rules

- Use Chinese for all user-facing communication, English for wiki content.
- NEVER modify files in the user's source/knowledge-base directories — they are read-only.
- All writes go to `{WIKI_DIR}`.
- Always update `index.md` and `log.md` after every operation.
- Read `SCHEMA.md` before generating any wiki pages.
