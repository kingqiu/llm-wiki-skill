# llm-wiki-skill

一个 [Claude Code](https://claude.ai/code) Skill，用于构建和维护个人知识 Wiki，遵循 [Andrej Karpathy 的 LLM Wiki 模式](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)。

**English documentation: [README.md](./README.md)**

---

## 功能介绍

把你的 Obsidian 笔记、PDF 和网页文章，自动整理成结构化、可搜索的 Wiki —— 基于 [Quartz v4](https://quartz.jzhao.xyz/) 构建，发布到 GitHub Pages。

三个核心操作：
- **Ingest（摄入）** — 导入源文件或 URL，自动生成 Wiki 页面
- **Query（查询）** — 用自然语言向你的 Wiki 提问
- **Lint（检查）** — 检测孤立页面、失效链接和知识空白

**双语支持**：每个页面都有中文翻译切换按钮（由智谱 GLM 或 DeepL 驱动）。

---

## 安装步骤

### 1. 安装 Skill

```bash
# 克隆到 Claude Code 的 skills 目录
git clone https://github.com/kingqiu/llm-wiki-skill.git ~/.claude/skills/llm-wiki
```

### 2. 安装 Quartz（一次性）

```bash
# 需要 Node.js v18+
node --version

# 可以让 skill 在首次运行时自动初始化 Quartz，
# 也可以手动操作：
git clone https://github.com/jackyzha0/quartz.git ~/my-wiki
cd ~/my-wiki
npm install
```

### 3. 安装双语组件（可选）

如果你想在 Wiki 中使用中文翻译切换按钮：

```bash
# 将 Bilingual 组件复制到你的 Quartz 安装目录
cp ~/.claude/skills/llm-wiki/quartz-components/Bilingual.tsx ~/my-wiki/quartz/components/
cp ~/.claude/skills/llm-wiki/quartz-components/scripts/bilingual.inline.ts ~/my-wiki/quartz/components/scripts/
```

然后按照 [quartz-components/SETUP.md](./quartz-components/SETUP.md) 的说明完成接入。

### 4. 首次运行

在任意目录打开 Claude Code，输入：

```
/llm-wiki
```

安装向导会引导你配置：
- 知识库目录（Obsidian Vault 等）
- Wiki 存放路径
- GitHub Pages 地址（可选）
- 翻译 API Key（智谱 AI 或 DeepL，可选）

配置保存在 `~/.claude/skills/llm-wiki/config.md`（已加入 .gitignore，API Key 只留本地）。

---

## 使用方法

```
/llm-wiki                              # 自动识别意图
/llm-wiki 我想整理 RAG 相关的笔记      # 触发 Ingest 流程
/llm-wiki wiki 里关于 memory 说了什么？ # 触发 Query 流程
/llm-wiki 检查一下有没有失效的链接      # 触发 Lint 流程
```

---

## 批量翻译已有页面

使用 `translate_wiki.py` 为所有现有页面添加中文翻译：

```bash
# 先修改脚本顶部的 CONTENT_DIR 路径
python3 ~/.claude/skills/llm-wiki/translate_wiki.py
```

需要在 `config.md` 中配置智谱 AI API Key。

---

## 环境要求

| 工具 | 版本要求 |
|------|---------|
| Claude Code | 最新版 |
| Node.js | v18+ |
| Git | 任意版本 |
| 智谱 AI 或 DeepL API Key | 可选（双语功能需要） |

---

## 开源协议

MIT
