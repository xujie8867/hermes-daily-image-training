# 冷门提示词挖掘（Rare Prompt Mining）

当用户抱怨主题/风格重复，或需要确保 4 张每日生图足够新鲜时使用本流程。

## 触发条件

- 用户说「这些主题重复了」「有没有新的」「这个风格出现太多次了」
- 每日 cron 任务需要保证 4 张变体跨大类多样性时

## 分析脚本

```python
import json
from collections import Counter

path = '/Volumes/外接硬盘/hermes-images/daily-image-training/resources/awesome-gpt-image2/all-prompts.json'

prompts = []
with open(path, 'r') as f:
    content = f.read().strip()
    if content.startswith('['):
        prompts = json.loads(content)
    else:
        for line in content.split('\n'):
            line = line.strip()
            if line:
                try:
                    prompts.append(json.loads(line))
                except:
                    pass

# 统计每个 title 的出现频率
titles = Counter(p.get('title', '') for p in prompts)
print(f"总提示词: {len(prompts)}")
print(f"唯一标题: {len(titles)}")

# 只取出现 1 次的冷门标题
rare = {t for t, c in titles.items() if c == 1 and t.strip()}
print(f"冷门标题（仅1次）: {len(rare)}")

# 筛选出冷门条目
rare_prompts = [p for p in prompts if p.get('title', '') in rare]

# 按 source 分类看分布
sources = Counter(p.get('source', '') for p in rare_prompts)
for s, n in sources.most_common():
    print(f"  {s}: {n}")

# 输出所有冷门条目用于人工筛选
for p in rare_prompts:
    print(f"TITLE: {p['title']}")
    print(f"SOURCE: {p.get('source','')}")
    print(f"PROMPT: {p['prompt'][:200]}...")
    print("---")
```

## 筛选原则

### 多样性约束
选出的 4 张必须是**完全不同的大类**：

| 大类 | 典型标题关键词 | 示例 |
|------|--------------|------|
| 机械/解剖美学 | 蒸汽朋克、解剖、机械、齿轮 | 蒸汽朋克射手座解剖图谱 |
| 摄影/艺术融合 | 超写实、水墨、融合、摄影 | 超写实与水墨的梦幻融合 |
| 动画/科幻主视觉 | 赛博、主视觉图、动画 | 赛博科幻桃太郎主视觉图 |
| 时尚/幻想摄影 | 襦裙、银河、写真、时装 | 银河繁星点缀的冰蓝襦裙 |

### 排除标准
- 与最近 7 天已生成主题同类的（从 session_search 或当日 README 获取）
- 含模板变量（如 `{argument name="xxx"}`）未填充的
- prompt 过短（< 30 字）缺乏执行细节的
- 纯英文且对中文用户无吸引力的（如足球海报、特定品牌 UI）

## 从冷门到优质 Prompt 的改造

冷门提示词通常来自社区库，格式不统一。使用前需改造：

1. **填充模板变量**：`{constellation_name}` → `射手座`，`{argument name="xxx" default="yyy"}` → `yyy`
2. **添加比例约束**：所有 prompt 开头加 `(2:3 portrait, 1024x1536)`
3. **精简为 250 字中文内**：gpt-image-2 的可靠上限，超限会返回空响应
4. **去掉负面/不适合内容**：裸露、血腥、政治敏感等
5. **确保有明确画面**：不是纯文字指令，而是可视觉化的描述

## 已发现的高价值冷门宝藏（2026-07-13）

| 标题 | 大类 | 新鲜度 |
|------|------|--------|
| 蒸汽朋克射手座解剖图谱 | 机械美学 | ⭐从未用过 |
| 超写实与水墨的梦幻融合 | 摄影融合 | ⭐从未用过 |
| 赛博科幻桃太郎主视觉图 | 动画科幻 | ⭐从未用过 |
| 银河繁星点缀的冰蓝襦裙 | 时尚幻想 | ⭐从未用过 |
| 千手观音化身打工人 | 荒诞幽默 | ⭐从未用过 |
| 国风工笔八仙长卷插画 | 传统工笔 | ⭐从未用过 |
| 试卷上的涂鸦巨龙 | 创意涂鸦 | ⭐从未用过 |
| 萌系大模型训练图解 | 科技萌化 | ⭐从未用过 |
| 史诗级科幻电影海报设计 | 电影海报 | ⭐从未用过 |
| 千禧年日系校园喜剧场景 | 日系复古 | ⭐从未用过 |
| 韩系极简氛围感少女写真 | 韩系写真 | ⭐从未用过 |
