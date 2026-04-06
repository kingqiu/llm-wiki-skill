---
name: llm-wiki
version: 0.6.0
description: |
  Build, query, and maintain a personal LLM-powered wiki from a local knowledge base.
  Features three distinct modes: Ingest (add knowledge), Query (ask questions with auto-enhancement), and Lint+Heal (health check + auto-repair).
  Query mode includes full knowledge compounding loop (Tier 1-3): automatic logging, smart enhancement (A/B/C/D types), and periodic review with query pattern analysis and archiving.
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

**CRITICAL: Bilingual Content Generation (Default Behavior)**

All wiki pages MUST be generated in bilingual format (English + Chinese) by default. For each paragraph:
1. Write the English content first
2. Immediately translate to Chinese using the configured translation engine
3. Append the translation as: `<div class="zh-trans">中文翻译</div>`

**Translation Engine Selection:**
Read `~/.claude/skills/llm-wiki/config.md` to get translation settings:
- `primary_engine`: First choice (zhipu/deepl/minimax)
- `fallback_engine`: Backup if primary fails
- If both fail, log error and continue with English-only

**Translation Rules:**
- Preserve technical terms in English: Agent, Harness, CLI, LLM, SDK, API, RAG, MCP, etc.
- Keep proper nouns, product names, and code identifiers untranslated
- Translate naturally for Chinese technical documentation style
- Do NOT translate: frontmatter, code blocks, URLs, wikilinks

**GLM-5 Translation Function (Zhipu AI):**
```python
def translate_paragraph(text: str, api_key: str, endpoint: str) -> str:
    """Translate using GLM-5 via Anthropic-compatible API."""
    prompt = f"""请将以下英文技术文本翻译成中文。要求：
1. 技术术语保持英文（如 Agent、Harness、CLI、LLM、SDK、API 等）
2. 翻译自然流畅，符合中文技术文档习惯
3. 只输出翻译结果，不要任何解释

{text}"""
    
    payload = {
        "model": "GLM-5",
        "max_tokens": 2000,
        "messages": [{"role": "user", "content": prompt}]
    }
    
    req = urllib.request.Request(
        endpoint,
        data=json.dumps(payload).encode(),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    )
    
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read())
            return result["content"][0]["text"].strip()
    except Exception as e:
        # Log error and return empty (fallback to English-only)
        print(f"Translation failed: {e}")
        return ""
```

**Batch mode:** Process all sources at once, generate all pages in bilingual format, then show the user a summary.

**Deep-read mode:** Process one source at a time, generate bilingual content, show the result, wait for feedback, then proceed to the next.

For each source:
1. Generate a bilingual source summary page in `{WIKI_DIR}/content/{topic}/sources/`
2. Create or update bilingual concept pages in `{WIKI_DIR}/content/{topic}/concepts/`
3. Create or update bilingual entity pages in `{WIKI_DIR}/content/{topic}/entities/`
4. Create bilingual synthesis pages for cross-cutting insights in `{WIKI_DIR}/content/{topic}/synthesis/`
5. Write or update bilingual `{WIKI_DIR}/content/{topic}/overview.md`
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

3. **Auto-log:** Automatically record this query to `{WIKI_DIR}/query-stats.json`:
   ```json
   {
     "timestamp": "2026-04-06T14:23:45Z",
     "query": "{user_question}",
     "pages_consulted": ["{page1}", "{page2}"],
     "tokens_generated": {estimated_tokens},
     "enhancement_type": null,
     "action_taken": "answered only"
   }
   ```
   If the file doesn't exist, create it as an empty array `[]` first.

4. **Evaluate enhancement:** Check if this query meets quality thresholds:
   - ≥3 pages consulted, OR
   - >500 tokens generated, OR
   - Reveals contradiction/gap between pages
   
   If threshold met, determine enhancement type:
   - **A**: New synthesis page (comprehensive cross-page analysis)
   - **B**: Enhance existing page (found missing content in a concept page)
   - **C**: Add cross-reference (found related pages without wikilinks)
   - **D**: Log knowledge gap (cannot answer sufficiently)

5. **Execute enhancement:**
   
   **C-type (auto):** 
   - Add wikilink to the Connections section of the relevant page
   - Update the query-stats.json entry with `"enhancement_type": "C"` and `"action_taken": "added cross-reference between {page1} and {page2}"`
   - Briefly note at end of answer: `[已自动添加 {page1} ↔ {page2} 的交叉引用]`
   
   **D-type (auto):** 
   - Append to `{WIKI_DIR}/knowledge-gaps.md` (create if doesn't exist):
     ```markdown
     ## [YYYY-MM-DD] {topic}
     - 问题：{user_question}
     - 原因：Wiki 中缺少相关内容
     - 建议：联网搜索补充相关概念
     ```
   - Update query-stats.json entry with `"enhancement_type": "D"` and `"action_taken": "logged knowledge gap"`
   - Briefly note: `[已将此问题记录到知识空白清单，供下次 Lint 时补充]`
   
   **A-type (confirm):** 
   - Ask user:
     ```
     💡 这个分析综合了 {N} 个页面，生成了 {X} tokens 的深度对比。
     建议创建新的 synthesis 页面：{topic}/synthesis/{slug}.md
     是否保存？(y/n)
     ```
   - If yes: create page following SCHEMA.md format, update index.md, append to log.md, update query-stats.json with `"enhancement_type": "A"` and `"action_taken": "created synthesis/{filename}"`
   - If no: update query-stats.json with `"enhancement_type": "A"` and `"action_taken": "user declined"`
   
   **B-type (confirm):** 
   - Ask user:
     ```
     💡 发现 {page} 缺少关于 {topic} 的内容。
     建议追加新小节：## {section_title}
     是否保存？(y/n)
     ```
   - If yes: append section to page, append to log.md, update query-stats.json with `"enhancement_type": "B"` and `"action_taken": "enhanced {page} with new section"`
   - If no: update query-stats.json with `"enhancement_type": "B"` and `"action_taken": "user declined"`

---

## Lint + Heal Flow (Wiki Health Check & Auto-Repair)

### Phase 1: Scan (fully automatic)

Read ALL markdown files under `{WIKI_DIR}/content/`. Check five issue types:

**1. Broken links** (all pages)
Collect every `[[wikilink]]` in every page. For each, check whether the target file exists under `content/`. Flag any that don't.

**2. Orphan pages** (all pages)
Find pages that have zero inbound wikilinks from any other page. Sources being orphaned is lower severity than concepts or synthesis.

**3. Missing concept pages** (all pages)
Scan all page bodies for noun phrases that appear ≥ 2 times across the wiki but have no corresponding page in any `concepts/` directory. Limit to top 5 most-mentioned missing concepts.

**4. Contradictions** (concepts + synthesis pages)
Compare factual claims across `concepts/` and `synthesis/` pages. Flag direct conflicts (e.g., page A says X is true, page B says X is false).

**5. Knowledge gaps** (whole wiki)
Identify 2–3 specific questions the wiki currently cannot answer based on its coverage. Frame as questions, not vague topics.

**Stale content check (run alongside scan):**
Find any paragraph or page that contains `⚠️ 待验证` AND was last modified more than 180 days ago. Add to report as "建议复核".

**6. Query pattern analysis (Tier 3 of knowledge compounding loop):**
Read `{WIKI_DIR}/query-stats.json` if it exists:
- Count queries by topic/theme
- Identify high-frequency topics (≥3 queries on same topic)
- Find repeated questions that Wiki cannot answer well
- Example: if "cost optimization" was queried 3+ times but no related pages exist, flag it

**7. Query archive check:**
Check the oldest timestamp in `query-stats.json`:
- If oldest record is >180 days old, flag for archiving
- Archive target: `query-stats-archive-YYYY-QN.json` (by quarter)
- Keep only recent 180 days in query-stats.json

---

### Phase 2: Report

Present findings grouped by severity. Use this format:

```
📋 Wiki 健康报告 — YYYY-MM-DD
扫描了 N 个页面

🔴 断链（N处）
  - {page} 第{n}行 → [[{target}]] 不存在

🟡 孤立页（N处）
  - {page} — 没有任何页面链接到它

🟡 缺少概念页（N个）
  - "{concept}" — 在 N 个页面中被提到，但没有概念页

🟠 矛盾（N处）
  - {page A} 与 {page B} 关于"{topic}"的说法冲突

🔵 知识空白（Wiki 目前无法回答）
  1. {question}
  2. {question}

⏰ 建议复核（⚠️标记超过180天）
  - {page} — 标记于 {date}

📊 Query 模式分析（基于 N 次查询记录）
  高频主题（≥3次）：
  - "{topic}" — 被问了 N 次，Wiki 中缺少相关页面
  建议补充的问题：
  - "{question}"（来自 knowledge-gaps.md）

⏰ Query 记录归档建议
  - 最早记录：YYYY-MM-DD（距今 X 天）
  - 建议归档 180 天前的记录到：query-stats-archive-YYYY-QN.json
```

---

### Phase 3: Confirm what to fix

After the report, present three fix categories and ask the user which to execute:

```
是否需要修复？请告诉我要做哪些，或直接说「全做」/「只做A」：

【A 类 — 自动修复，不需联网】
  A1. 删除/注释 N 处断链 wikilink
  A2. 为 N 个孤立页在最相关页面补入链

【B 类 — 联网补充】
  B1. 为"{concept}"生成新概念页（需联网搜索）
  B2. 填补知识空白："{question}"（需联网搜索）
  B3. 补充高频 Query 主题："{topic}"（需联网搜索）

【C 类 — Query 数据维护】
  C1. 归档 180 天前的 query 记录 → query-stats-archive-YYYY-QN.json
```

Wait for user confirmation before proceeding.

---

### Phase 4: Heal Execution

#### A-type fixes (no web search)

**A1 — Broken links:**
- If the target page clearly doesn't exist and can't be inferred: remove the wikilink brackets, keep plain text.
- If a similar page exists (typo or path issue): correct the wikilink path.

**A2 — Orphan pages:**
- Read the orphan page's content to understand its topic.
- Find the 1–2 most related pages in the wiki.
- Add a brief mention + wikilink to the orphan from those pages (append to a "Related" or "See also" section).

#### B-type fixes (web search required)

For each B-type item, follow this pipeline strictly:

**Step 1 — Search**
```
WebSearch("{concept or question} site:arxiv.org OR site:anthropic.com OR site:github.com OR site:huggingface.co OR site:paperswithcode.com")
```
If results are thin, retry without domain filter.

**Step 2 — Filter by trusted domains**
Prioritize results from (in order):
1. arxiv.org / aclanthology.org — academic papers
2. anthropic.com / openai.com / deepmind.com — primary sources
3. github.com — official repos
4. huggingface.co / paperswithcode.com

Deprioritize: blogs, social media, aggregators.

**Step 3 — Fetch full content**
Use `baoyu-url-to-markdown` skill on the top 2–3 URLs to get full page content.

**Step 4 — Cross-validate**
- If a key fact appears in ≥ 2 independent sources → write it as a direct statement.
- If a key fact appears in only 1 source → write it with `⚠️ 待验证` marker.

**Step 5 — Write to wiki (BILINGUAL)**

**CRITICAL: All new content MUST be bilingual.**

For missing concept pages (B1):
Create `{WIKI_DIR}/content/{topic}/concepts/{concept-slug}.md` following SCHEMA.md format.
- Write each paragraph in English first
- Immediately translate using GLM-5 and append `<div class="zh-trans">中文翻译</div>`
- Append at the bottom:
```markdown
---
*Sources added by Heal on YYYY-MM-DD:*
- [Title](url) · YYYY-MM
- [Title](url) · YYYY-MM
```

For knowledge gaps (B2):
If the answer fits an existing page, append a new bilingual section to that page.
If the answer is broad enough, create a new bilingual synthesis page.
Always append source citations in the same format above.

**Never overwrite existing content.** Only append new sections or create new pages.

#### C-type fixes (query data maintenance)

**C1 — Archive old query records:**
1. Read `{WIKI_DIR}/query-stats.json`
2. Split records into two groups:
   - `recent`: timestamp within last 180 days
   - `old`: timestamp older than 180 days
3. If `old` is empty: tell user "没有需要归档的记录（最早记录距今不足180天）"
4. If `old` has records:
   - Determine archive filename by quarter of oldest record:
     - Q1: Jan-Mar → `query-stats-archive-YYYY-Q1.json`
     - Q2: Apr-Jun → `query-stats-archive-YYYY-Q2.json`
     - Q3: Jul-Sep → `query-stats-archive-YYYY-Q3.json`
     - Q4: Oct-Dec → `query-stats-archive-YYYY-Q4.json`
   - Write `old` records to archive file (append if file exists, create if not)
   - Write `recent` records back to `query-stats.json`
   - Tell user: "已归档 {N} 条记录到 {archive_filename}，query-stats.json 保留最近 {M} 条"

**B3 — Supplement high-frequency query topics:**
- Same pipeline as B1/B2 (web search → validate → write to wiki)
- Target: create a new concept or synthesis page for the high-frequency topic
- Use the original queries as context to understand what the user wants to know

---

### Phase 5: Wrap up

After all fixes are applied:
1. Run `npx quartz build` to rebuild the wiki.
2. Append to `log.md`:
```
## [YYYY-MM-DD] lint+heal | 断链:{n}处, 孤立页:{n}个, 新建概念页:{list}, 填补空白:{list}, 归档query:{n}条
```
3. Show the user a summary of everything changed.

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

- Use Chinese for all user-facing communication.
- **All wiki content MUST be bilingual (English + Chinese) by default.** Each English paragraph followed by `<div class="zh-trans">中文翻译</div>`.
- Translation engine priority: read from config.md (primary_engine → fallback_engine).
- NEVER modify files in the user's source/knowledge-base directories — they are read-only.
- All writes go to `{WIKI_DIR}`.
- Always update `index.md` and `log.md` after every operation.
- Read `SCHEMA.md` before generating any wiki pages.
