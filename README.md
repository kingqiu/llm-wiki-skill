# llm-wiki-skill

A [Claude Code](https://claude.ai/code) skill for building and maintaining a personal knowledge wiki, following [Andrej Karpathy's LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f).

**中文文档请见 [README.zh.md](./README.zh.md)**

---

## What it does

Turn your Obsidian notes, PDFs, and web articles into a structured, searchable wiki — powered by [Quartz v4](https://quartz.jzhao.xyz/) and published to GitHub Pages.

**Three core operations:**
- **Ingest** — Transform source files/URLs into structured wiki pages (concepts, entities, synthesis)
- **Query** — Ask questions in natural language, get answers with auto-enhancement
- **Lint+Heal** — Detect and fix broken links, orphan pages, knowledge gaps, contradictions

**Key features:**
- **Bilingual by default** — All pages generated with English + Chinese (GLM-5 or DeepL)
- **Knowledge compounding loop** — Queries auto-enhance the wiki (4 enhancement types: A/B/C/D)
- **Query pattern analysis** — Identifies high-frequency topics for targeted expansion
- **Cross-validated sources** — Heal mode validates facts from ≥2 trusted domains
- **Wikilink-based navigation** — Full-path wikilinks for reliable Quartz SPA routing

---

## Installation

### 1. Install the skill

```bash
# Clone this repo into your Claude Code skills directory
git clone https://github.com/kingqiu/llm-wiki-skill.git ~/.claude/skills/llm-wiki
```

### 2. Install Quartz (one-time)

```bash
# Node.js v18+ required
node --version

# You can let the skill set up Quartz automatically on first run,
# or do it manually:
git clone https://github.com/jackyzha0/quartz.git ~/my-wiki
cd ~/my-wiki
npm install
```

### 3. Set up the bilingual component (optional)

If you want the Chinese translation toggle button in your wiki:

```bash
# Copy Bilingual component into your Quartz installation
cp ~/.claude/skills/llm-wiki/quartz-components/Bilingual.tsx ~/my-wiki/quartz/components/
cp ~/.claude/skills/llm-wiki/quartz-components/scripts/bilingual.inline.ts ~/my-wiki/quartz/components/scripts/
```

Then follow the instructions in [quartz-components/SETUP.md](./quartz-components/SETUP.md) to wire it up.

### 4. First run

Open Claude Code in any directory and type:

```
/llm-wiki
```

The setup wizard will ask for:
- Your source directories (Obsidian vault, etc.)
- Your wiki directory path
- Your GitHub Pages URL (optional)
- Translation API keys (ZhipuAI or DeepL, optional)

Config is saved to `~/.claude/skills/llm-wiki/config.md` (gitignored — your keys stay local).

---

## Usage

The skill has three main modes that are auto-detected from your input:

### 1. Ingest Mode — Build Knowledge

Add new topics or supplement existing ones from local files or web sources.

```
/llm-wiki ingest 新主题：AI Agent Architecture（批量模式）
```

**What happens:**
1. Scans your configured source directories for relevant files
2. Optionally searches the web for supplementary materials
3. Generates structured wiki pages:
   - `overview.md` — topic summary
   - `concepts/*.md` — key concepts
   - `entities/*.md` — tools, companies, frameworks
   - `sources/*.md` — source summaries
   - `synthesis/*.md` — cross-cutting insights
4. **All content is bilingual by default** — each English paragraph followed by `<div class="zh-trans">中文翻译</div>`
5. Updates `index.md` and `log.md`
6. Builds the wiki with Quartz

**Modes:**
- **批量模式 (Batch)** — processes all sources at once, shows summary at the end
- **精读模式 (Deep-read)** — processes one source at a time, pauses for feedback

**Bilingual Generation:**
- Uses GLM-5 (ZhipuAI) or DeepL API configured in `config.md`
- Technical terms preserved in English (Agent, Harness, CLI, LLM, etc.)
- Fallback to English-only if translation fails

---

### 2. Query Mode — Ask Questions

Ask questions about your wiki in natural language. The skill will:
1. Search relevant pages
2. Synthesize an answer with citations
3. **Auto-enhance the wiki** based on query quality:
   - **Type A** — Create new synthesis page (if ≥3 pages consulted or >500 tokens)
   - **Type B** — Enhance existing page (if missing content found)
   - **Type C** — Add cross-references (auto, no confirmation)
   - **Type D** — Log knowledge gap (auto, for future Heal)

```
/llm-wiki what's the difference between RAG and agent memory?
```

**Query logging:**
- All queries saved to `query-stats.json` with metadata
- Used for pattern analysis in Lint+Heal flow
- Auto-archived after 180 days

---

### 3. Lint + Heal Mode — Health Check & Auto-Repair

Scan the entire wiki for issues and optionally fix them.

```
/llm-wiki lint
```

**Scan results (automatic):**
- 🔴 Broken wikilinks
- 🟡 Orphan pages (no inbound links)
- 🟡 Missing concept pages (mentioned ≥2 times but no page exists)
- 🟠 Contradictions (conflicting claims across pages)
- 🔵 Knowledge gaps (questions wiki can't answer)
- ⏰ Stale content (⚠️ 待验证 markers older than 180 days)
- 📊 Query pattern analysis (high-frequency topics from query-stats.json)

**Fix categories:**
- **A-type (auto, no web search)** — fix broken links, connect orphan pages
- **B-type (web search required)** — create missing concept pages, fill knowledge gaps
  - All new content generated in **bilingual format**
  - Cross-validates from ≥2 trusted sources (arxiv.org, anthropic.com, github.com, etc.)
- **C-type (data maintenance)** — archive old query records

User confirms which fixes to apply before execution.

---

## Advanced: Batch Translate Existing Pages

If you have existing English-only pages, use the standalone translation script:

```bash
# Edit BATCHES in the script to match your file structure
python3 /path/to/translate_wiki.py
```

This is a one-time migration tool. New pages generated via `/llm-wiki ingest` are bilingual by default.

---

## Requirements

| Tool | Version |
|------|---------|
| Claude Code | Latest |
| Node.js | v18+ |
| Git | Any |
| ZhipuAI or DeepL API key | Optional (for bilingual) |

---

## License

MIT
