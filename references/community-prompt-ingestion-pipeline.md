# 社区 Prompt 仓库提取管道

将 GitHub 上的 GPT Image 2 社区 prompt 仓库批量提取、去重、分类、入库到每日生图资源库。

## 支持的数据格式

| 格式 | 示例仓库 | 提取方法 |
|------|---------|---------|
| JSON 数组 (`prompts.json`) | gpt-image2/awesome-gptimage2-prompts | `json.load()` → 遍历 items |
| 结构化 JSON (`data/*.json`) | peterRooo/awesome-gpt-image-2-prompts | `json.load()` → 取 `prompt` 字段 |
| Markdown gallery (`gallery-*.md`) | wuyoscar/GPT-Image2-Skill | 正则提取 ` ```text\n...\n``` ` 块 |
| README 内嵌 `<details>` | itgoyo/awesome-gpt-image2-prompt | 正则提取 ` ```text\n...\n``` ` 块 |

## 标准流程

```bash
# 1. 批量克隆（注意：不能用 & 并行，Hermes terminal 禁止）
cd /tmp
for repo in \
  "https://github.com/XXX/YYY.git" \
  "https://github.com/AAA/BBB.git"; do
  git clone --depth 1 "$repo"
done

# 2. 用 Python 脚本提取 → 见下方模板

# 3. 清理临时仓库
rm -rf /tmp/repo-*
```

## 提取脚本模板

```python
import os, re, json, glob
from collections import defaultdict

OUTPUT_DIR = "/Volumes/外接硬盘/hermes-images/daily-image-training/resources/NEW-DIR"
# 注意：每次入库前先 shutil.rmtree(OUTPUT_DIR) 清旧数据，保证幂等

all_prompts = []

# ==== JSON 格式 ====
with open('/tmp/repo/prompts.json') as f:
    data = json.load(f)
for item in data.get('items', []):
    prompt = item.get('prompt', '') or item.get('text', '')
    if prompt and len(prompt) > 30:
        cat = item.get('category', '') or 'general'
        all_prompts.append({"category": cat, "prompt": prompt.strip(), "source": "REPO_NAME"})

# ==== Markdown gallery 格式 ====
for gf in glob.glob('/tmp/repo/**/gallery-*.md', recursive=True):
    cat = os.path.basename(gf).replace('gallery-', '').replace('.md', '').replace('-', ' ')
    with open(gf) as f:
        content = f.read()
    blocks = re.findall(r'```text\n(.*?)```', content, re.DOTALL)
    for block in blocks:
        if 50 < len(block.strip()) < 3000:
            all_prompts.append({"category": cat, "prompt": block.strip(), "source": "REPO_NAME"})

# ==== 去重（前80字符） ====
seen = set()
unique = []
for p in all_prompts:
    key = p["prompt"][:80].strip().lower()
    if key not in seen:
        seen.add(key)
        unique.append(p)

# ==== 分组写入 ====
by_cat = defaultdict(list)
for p in unique:
    by_cat[p["category"].strip().lower() or "general"].append(p)

for cat, prompts in by_cat.items():
    safe = re.sub(r'[^a-z0-9]+', '-', cat).strip('-')
    with open(os.path.join(OUTPUT_DIR, f"{safe}.md"), 'w') as f:
        f.write(f"# {cat.title()}\n\n> {len(prompts)} prompts\n\n---\n\n")
        for i, p in enumerate(prompts, 1):
            f.write(f"### #{i}\n\n```text\n{p['prompt'][:800]}\n```\n\n*Source: {p['source']}*\n\n---\n\n")
```

## 已验证的优质仓库

| 仓库 | ⭐ | 入库数 | 数据格式 |
|------|-----|--------|---------|
| gpt-image2/awesome-gptimage2-prompts | 194 | 2,717 | `prompts.json` |
| peterRooo/awesome-gpt-image-2-prompts | 73 | 524 | `data/*.json` |
| wuyoscar/GPT-Image2-Skill | 3,526 | 162 | `gallery-*.md` |
| jau123/MeiGen-AI-Design-MCP | 1,535 | 20 | `**/*.md` |

## 赛后维护

1. 入库后更新 `daily-image-training/SKILL.md` 的资源表
2. 清理 `/tmp/` 下的临时克隆
3. 每次入库用 `shutil.rmtree` 清旧目录重新生成，保证幂等

## 已入过库的仓库（避免重复拉取）

以下仓库已提取入库，无需再次处理：
- freestylefly/awesome-gpt-image-2 (⭐8,178) — 已独立入库
- ZeroLu/awesome-gpt-image (⭐1,851) — 已独立入库
- davidwuw0811-boop/awesome-gpt-image2-prompts (⭐213) — 已独立入库（davidwu-prompts.json）
- EvoLinkAI/awesome-gpt-image-2-API-and-Prompts — 已独立入库
- Anil-matcha/Awesome-GPT-Image-2-API-Prompts — 已独立入库
- gpt-image2/awesome-gptimage2-prompts (⭐194) — 已合入社区精选
- peterRooo/awesome-gpt-image-2-prompts (⭐73) — 已合入社区精选
- wuyoscar/GPT-Image2-Skill (⭐3,526) — 已合入社区精选
- jau123/MeiGen-AI-Design-MCP (⭐1,535) — 已合入社区精选
