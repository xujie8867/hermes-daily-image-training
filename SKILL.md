---
name: daily-image-training
description: "Load when the user requests image generation, image editing, or image-to-video. Auto-builds structured prompts using the five-segment template, selects generation channels, produces 4 variants, and iterates based on user feedback."
version: "6.1.0"
last_updated: "2026-09-11"
---

# 每日生图 v6.1 — 精简版（2026-09-11 通道实测）

> v6 目标：单一事实源、零死代码、可脚本化执行。旧版 5 套去重、双份负向词、多通道切换规则已全部合并或删除。

## 🚨 第一优先·交付铁律

1. **最后一步 = 发图**：确认文件真实存在后，最终响应必须逐行列出 **7 个** `MEDIA:/绝对路径` 路径（每行一个）。
2. 只写文字总结 = 白生成；失败/缺图必须明确报告，不静默，不用低质结果凑数。

## 每场结构（固定 7 张）

| # | 内容 | 生成方式 |
|---|------|---------|
| 01 | 林晚《古风人物志艺术字海报》 | F02 主身份图 + F01 辅助图，gpt-image-2.5-high |
| 02 | 东方故事衍生 | 以 01 成品为参考，image-to-image |
| 03 | 白描画衍生 | 以 01 成品为参考，image-to-image |
| 04 | 无人图·世界著名建筑 | 文生图，no people |
| 05 | 无人图·意境风景 | 文生图，no people |
| 06 | 无人图·自由方向 A | 文生图，no people |
| 07 | 无人图·自由方向 B | 文生图，no people |

- 02 固定 photo-story「东方故事」：暖象牙白纸底、低视觉密度、有限色块、结构线、留白；不是国风写真+做旧滤镜；保留林晚身份、姿态、器物。
- 03 固定 photo-story「白描画」：暖白宣纸底、单色黑灰墨线、大面积留白；重点看双手与器物接触关系。
- 02/03 禁止任何汉字/书法/印章/字母/乱码；01 的标题不得被重绘进衍生图。
- 04-07 至少 1 张世界著名建筑 + 1 张意境风景；06/07 从方向池随机抽（野生动物/工业场景/天文观测/昆虫微距/水下摄影/极地风光/市井美食/废墟遗迹/港口渔市/植物图鉴/都市夜景/雪域高原等），近 7 天不重复。

## 模型与通道（唯一规则）

- **配置语义**：`image_gen.model: gpt-image-2.5-high`（tier 名）。不切 Grok、不切 Gemini、不切 Codex，除非用户当次明确指定。
- **2026-09-11 实测**：当前 CPA/openai 中转只接受 `gpt-image-1.5 / gpt-image-2 / grok-imagine-*`。`gpt-image-2.5-sunburst-high` 会 400。运行时实际走 `gpt-image-2-high`（可用最高档）。未知 2.5 id 会被插件静默落到 medium，必须显式写成 `gpt-image-2-high`。
- `aspect_ratio=portrait`，prompt 首行 `Vertical 2:3 portrait, full frame edge to edge`。
- relay 原始输出 1024×1536，等比 Lanczos 放大至 2048×3072 交付。
- 01 中文标题与短文案由本地 Songti SC 确定性排版写入，不依赖模型直出文字。

## 核心公式（写 prompt 的唯一依据）

```
[场景+人物/主体] + [自然光线：光源/方向/软硬/衰减] + [相机+镜头+ISO] + [材质响应] + [纪实风格声明]
→ 禁止：艺术大师名、cinematic/staged/editorial
```

- 去AI感三层必带：色彩收敛（muted natural colors）+ 物理真实感（skin pores / film grain / contact shadows）+ 构图去理想化（candid, natural asymmetry）。
- 每张至少一个色彩锚点，禁止全图死灰。
- 人像禁提痣/mole/beauty mark，面部细节完全靠 F02/F01 参考图。
- 选题回避：浅色逆光组合、黑白纪实人像、镜面反射表面。

### 负向词（唯一版本，每张必带）

```
NOT CGI, NOT 3D render, NOT airbrushed, NOT plastic skin, NOT waxy skin,
NOT doll-like, NOT beauty filter, NOT over-sharpened, NOT HDR glow,
NOT cinematic lighting, NOT staged portrait, NOT oversaturated, NOT digital art
```

人像追加：`visible pores, natural skin texture, unretouched, contact shadows`

## 01 林晚人物志机制（拉鲁斯 recvtPMJbYBcPt）

- 核心机制：林晚真实东方人物摄影 + 中文书法主标题 + 局部手绘轮廓线 + 由器物/动作衍生的 Graphic Line + 东方策展 Editorial Poster 排版。
- 线条规则：贴合人物一小段 → 中断 → 离开人物 → 转化为器物线条（琴弦/丝线/山脊/墨迹飞白/茶烟/香篆/伞骨/舞袖/花枝等）；禁止完整描边、禁止 doodle。
- 书法标题与短文案**由本地 Songti SC 确定性排版写入**，不依赖模型直出文字。
- AM/PM 人物身份、动作、器物、主标题、短文案、线条来源、服饰、场景、版式互不相同。

## 去重（统一为一套，2026-09-10 合并）

1. **人物志 30 天**：`.larus-daily-selection.json` 的 am/pm 字段，按身份/动作/器物/文字/线条/服饰/场景/版式去重。
2. **非人物题材 30 天**：建筑、风景、自由方向按"核心主体+地貌"记入各场次 README；同一主体 30 天冷却（换天气/光线/机位不算新题）。泰姬陵禁用至 2026-11-28。
3. **光影模板 7 天**：晨雾/金辉轮廓/长曝光流水/黄金时刻建筑/雪景静谧/蓝调时刻/单束光束，7 天内每种最多 1 次。
4. AM/PM 互斥：上午出完写入记录，下午选题前先读，当天不重叠。
- ~~dedup_check.py 180天 style_key 机制~~：已废弃，不再执行（多系列实验遗留）。
- 选题完成后做一次关键词检索核对（历史文件名 + README），命中冷却即重选。

## QC（3 项硬门禁，2026-09-10 瘦身）

1. **无人图 0 人**：04-07 检测 0 脸/0 人（Vision 或 OpenCV 一次即可）。
2. **人像 1 脸 2 手**：01 检出 1 脸、1 人、≤2 手且无穿模。
3. **衍生图无文字**：02/03 OCR 为空（无乱码/伪文字）。

- 通过 → 交付；不通过 → 最多定向重试 1 次（01 生成阶段总计 ≤2 版，字形瑕疵走本地排版替换）；仍失败 → 明确报告缺图。
- ~~InsightFace 余弦比对~~、四角亮度统计、逐字切片墨量校验：降为可选参考值，不作为重试触发条件，不再阻塞交付。
- QC 与放大、元数据写入合并为单条 Python 脚本一次跑完。

## 防步数超限（执行效能）

1. 01 最多定向重试 1 次；字形问题用本地排版图层解决，禁止 v3/v4 循环。
2. 04-07 单轮并发/连续发起，禁止逐张串行问答式校验。
3. 放大 + QC + README/meta 生成脚本化，单步完成。
4. 模型参数固定写当前可用最高档：`gpt-image-2-high`（config 语义仍可保留 2.5-high tier）。

## 交付与公众号

- 每场交付 7 图 + 7 条简短中文提示词（每条一句话）。
- 公众号 `newspic` 草稿：`article_type=newspic`，标题固定 `【Ai摄影作品集】YYYY年M月D日周X 上午场|下午场`（日期取归档目录日期，星期真实计算）；只存草稿不群发；上传后回读核验类型/标题/图片数=7/顺序。
- 发布命令：`python3 /Users/xuhailong/公众号任务/scripts/publish_codex_draft.py deploy --meta <publish_meta.json> --article-type newspic --run-id <日期-slug>`。
- 标题重复报错 `checkpoint_verify_miss`/dedupe 时：先删远端 `runs/<run-id>/publish_state.json`，再带 `--delete-media-id-before-add <旧media_id>` 重发。
- 归档：`/Volumes/外接硬盘/hermes-images/daily-image-training/YYYY-MM-DD-am|pm/`（images/ + orig/ + work/ + README.md + newspic/）。
- 飞书发送最小边 ≥2000 的放大版；MEDIA 路径顶格独立行。

## 风格矩阵速查（写 prompt 用，不再展开）

- 人像：R5 85/1.2 ISO800-1600 窗光/阴天/钨丝灯 · Hasselblad 80/1.9 北窗光 · Leica M11 35/1.4 午后树影
- 风景：Sony 24-70@35 ISO200 三脚架晨光 · Sony 24/1.4 ISO100 蓝调长曝光
- 动物：Sony 400/2.8+1.4x ISO800 金辉轮廓
- 微距：R5 100/2.8 macro ISO400 叶隙晨光
- 建筑：R5 17-40 移轴 ISO100 黄金侧光透视校正 · Sony 16-35/2.8 几何日光 · Leica Q2 28/1.7 晨光纪实
