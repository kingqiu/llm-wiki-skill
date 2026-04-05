# llm-wiki-skill

A [Claude Code](https://claude.ai/code) skill for building and maintaining a personal knowledge wiki, following [Andrej Karpathy's LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f).

**中文文档请见 [README.zh.md](./README.zh.md)**

---

## What it does

Turn your Obsidian notes, PDFs, and web articles into a structured, searchable wiki — powered by [Quartz v4](https://quartz.jzhao.xyz/) and published to GitHub Pages.

Three operations:
- **Ingest** — feed source files or URLs → wiki pages are generated automatically
- **Query** — ask questions against your wiki in natural language
- **Lint** — detect orphan pages, broken links, and knowledge gaps

**Bilingual support**: each page has a Chinese translation toggle (powered by ZhipuAI GLM or DeepL).

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

```
/llm-wiki                        # auto-detects intent from your message
/llm-wiki I want to add notes on RAG    # Ingest flow
/llm-wiki what does the wiki say about memory?  # Query flow
/llm-wiki check for broken links        # Lint flow
```

---

## Batch translate existing pages

Use `translate_wiki.py` to add Chinese translations to all existing pages:

```bash
# Edit the CONTENT_DIR path at the top of the script first
python3 ~/.claude/skills/llm-wiki/translate_wiki.py
```

Requires a ZhipuAI API key set in `config.md`.

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
