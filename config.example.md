---
# LLM Wiki 配置文件模板
# 复制此文件为 config.md，填入你自己的配置
# config.md 已被 .gitignore 排除，API Key 不会上传到 GitHub
configured: true
---

# LLM Wiki 配置文件

此文件由 /llm-wiki 首次运行向导自动生成。如需修改，直接编辑对应字段即可。

## Source Directories
# 知识库目录（支持多个路径，每行一个）
- /path/to/your/obsidian/Raw
- /path/to/your/obsidian/Learning

## Wiki Directory
/path/to/your/wiki

## GitHub Pages
https://yourusername.github.io/YourWiki

## Translation Settings
# 翻译引擎优先级：依次尝试，第一个可用的生效
# 可选值: deepl / zhipu / minimax / none（禁用翻译）
primary_engine: zhipu
fallback_engine: deepl

# 双语模式默认开关（true=默认显示中文，false=默认隐藏）
bilingual_default: false

# ZhipuAI 配置（推荐，免费额度较大）
# 申请地址：https://open.bigmodel.cn/
zhipu_api_key: YOUR_ZHIPU_API_KEY_HERE
zhipu_api_endpoint: https://open.bigmodel.cn/api/anthropic/v1/messages
zhipu_model: GLM-4-Flash

# DeepL 配置（备用）
# 申请地址：https://www.deepl.com/pro-api
deepl_api_key:

# MiniMax 配置（备用）
minimax_api_key:
minimax_api_endpoint:
