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

## 每场结构（固定 7 张，排期按周中/周末分流）

### 1. 人像篇排期规则（2026-09-12 用户最新铁律）

- **周一至周五（工作日场次）**：
  - **01–03 前三张全为人像**：**不限定林晚，不限定风格，以「高质量单反或iPhone摄影人像高级感」为唯一准则（2026-09-14 用户铁律）**！
    - **不限定必须是女士：男女老少、多元族裔、职业纪实、生活抓拍均可，不做任何限定**；
    - 通过 `prepare_daily_batch.py` 从已清洗词库采样 3 条高质量独立提示词（脚本负责剔除占位符/版式/无人场景）；
    - 场景不设限、人物不设限、风格不设限（电影纪实、复古胶片、自然光影特写、高级时装社论、工匠纪实等多元探索）；
    - **不限定性别、年龄、族裔、人物身份、发型、服装或具体审美模板**；唯一标准是高质量、真实、专业、具有高级感的摄影；
    - 三张必须是彼此独立的主体，不得复用同一张脸、同一身份或默认美女模板；生成前检查人物描述是否同质化，撞脸则重新采样；
    - 仅使用可直接执行的干净摄影 Prompt，剔除 JSON、`{argument}` 占位符、`REFERENCE_` 工作流、广告版式和无人场景提示；
    - 追求电影级物理控光、真实肌肤质感、高级审美，严禁 AI 塑料假脸，**严禁做 01 水彩/白描复刻**；
    - **姿态必须写成可执行的身体几何关系，不写“自然一点/松弛一点”这类抽象词**。按需使用“转、弯、顺、露”：转=头/胸/腿至少一个面错开；弯=歪头、屈肘或微屈膝打破直杆线；顺=前臂接手背、腿线接脚尖；露=手有明确落点且手指可见。每张只选最需要的 1–2 项，避免动作指令堆叠；
    - 最短姿态模板：`[站/坐/蹲/躺] + [身体朝向] + [一个明确动作]`。示例：`身体侧转，脸转向镜头，手轻扶帽檐`；坐姿想显腿长则写 `侧坐，双腿斜向一侧，脚尖顺势延伸`；遮挡可以存在，但必须让画面解释手去了哪里；
    - “美姿”是工具，不是审美模板：证件照可正、运动人物可保留力量折角；不得因此限制工作日人物的性别、年龄、族裔、职业或摄影风格。
- **周六周日（周末场次）**：
  - **01 林晚《古风人物志艺术字海报》**：固定使用**林晚角色形象**（F02 主身份图 + F01 辅助图），拉鲁斯东方策展海报风格（真实东方女性摄影 + 中文书法标题 + 局部 Graphic Line + 东方意境留白，低盘发，无痣）；
  - **02 水彩画风格复刻**：以 01 成品为参考，image-to-image，**必须完全复刻 01 林晚的人物形象、同一面容、贴颈低发髻（low bun）与同一服装**，水彩通透温润质感，严禁脑补古典高发髻与红袍大袖；
  - **03 黑白线稿模型复刻**：以 01 成品为参考，image-to-image，**必须完全复刻 01 林晚的人物形象、同一面容、贴颈低发髻（low bun）与同一服装**，纯黑白工笔白描墨线质感，大面积留白；

| # | 内容 | 生成方式与排期机制 |
|---|------|---------|
| 01 | 人像主篇 | **工作日**：提示词库高级感人像（不限林晚/不限风格）；**周末**：固定林晚拉鲁斯艺术字海报 |
| 02 | 人像篇 2 / 水彩复刻 | **工作日**：提示词库高级感人像（不限林晚/不限风格）；**周末**：以 01 为参考 1:1 水彩复刻 |
| 03 | 人像篇 3 / 线稿复刻 | **工作日**：提示词库高级感人像（不限林晚/不限风格）；**周末**：以 01 为参考 1:1 白描线稿复刻 |
| 04 | 无人图·世界著名建筑 | 文生图，no people |
| 05 | 无人图·意境风景 | 文生图，no people |
| 06 | 国风城市文旅长卷海报 A | 文生图无字底图 + 本地确定性排版；可含一位地域文化人物 |
| 07 | 国风城市文旅长卷海报 B | 与 06 不同城市；文生图无字底图 + 本地确定性排版 |

### 2. 02/03 复刻 Prompt 黄金防漂移模板（必遵）
```text
Keep exact same subject and identity from image 01: identical face and facial bone structure, identical natural low bun hairstyle at the nape of neck (STRICTLY NO high bun, NO elaborate hairpins, NO red ribbons), identical clothing and posture. Translate ONLY the medium:
- 02: into minimalist fine watercolor painting on warm white textured paper, soft translucent wash edges.
- 03: into pure black and white line art / traditional baimiao ink drawing, elegant rhythmic contours, zero shading, generous negative space.
STRICTLY FORBIDDEN: text, Chinese characters, signatures, stamps, watermark, high bun, ancient headdress, change of clothing, change of facial identity.
```
- 04 固定世界著名建筑、05 固定意境风景，二者必须无人。06/07 固定为两座不同城市的国风文旅叙事长卷海报：左侧约 30% 暖白文字留白区，右侧约 70% S 形连续城市长卷，右上自然地貌与地标、中部历史建筑与非遗、右下地域人物与风物；城市地标、建筑、服饰、非遗、食物和动植物必须真实属于该城市，严禁跨城混搭。
- 06/07 生图阶段只生成**无字底图**，禁止模型生成中文、英文、印章或 Logo；完成后在左侧留白区用本地字体确定性写入城市名、四字主题、英文城市名、年份与印章。两张城市不得相同，同一城市 30 天冷却。

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
- 每张至少一个色彩锚点，禁止全图死灰。黑白纪实例外：以影调层次代替色彩锚点。
- 禁提痣/mole/beauty mark 的约束仅适用于周末林晚场；工作日独立人像不受林晚身份/发型/服装约束。
- 选题回避：浅色逆光组合、镜面反射表面。黑白纪实、任何性别/年龄/族裔/风格均不回避（2026-09-14 用户铁律：不限定，唯一标准是高级感摄影）。

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
2. **建筑/风景/城市 30 天**：04/05 按“核心主体+地貌”去重；06/07 按城市 slug 去重，同一城市 30 天冷却。泰姬陵禁用至 2026-11-28。
3. **光影模板 7 天**：晨雾/金辉轮廓/长曝光流水/黄金时刻建筑/雪景静谧/蓝调时刻/单束光束，7 天内每种最多 1 次。
4. AM/PM 互斥：上午出完写入记录，下午选题前先读，当天不重叠。
- ~~dedup_check.py 180天 style_key 机制~~：已废弃，不再执行（多系列实验遗留）。
- 选题完成后做一次关键词检索核对（历史文件名 + README），命中冷却即重选。

## QC（4 项硬门禁，2026-09-12 强化防漂移）

1. **无人图 0 人**：仅 04/05 检测 0 脸/0 人；06/07 可含一位地域文化人物，不适用无人门禁。
2. **人像质感与姿态门禁**：01–03 确认画质锐利、有微对比度与眼神光、无肢体畸变、无 AI 塑料皮；姿态检查头/胸/腿是否无意共面僵直、关节转折是否符合动作、手腕与脚尖是否顺接肢体线条、被遮挡的手是否有明确去向。OpenCV 检脸数仅作参考，不因背景/高噪点黑白街头的伪检阻断交付。
3. **周末场 02/03 人像复刻防漂移**：周末场 02/03 必须完全复刻 01 林晚；保持自然低发髻（low bun）与同一服装，严禁突变古典高发髻（high bun）、繁杂头饰或宽袍汉服。一经发现漂移立刻定向重跑一次。工作日 01–03 不适用复刻规则。
4. **衍生图无文字**：周末 02/03 OCR 为空（无乱码/伪文字）。

### 06/07 城市海报 QC

- 城市事实一致：地标、建筑、非遗、服饰和风物均属于同一城市，禁止跨城混搭。
- 底图 OCR 应为空；左侧 30% 留白不得被人物、建筑或植物遮挡。
- 本地排版后回读检查城市名、四字主题、英文城市名、年份和印章，无乱码、错别字和溢出。
- 若出现文化人物，检查手部结构、动作逻辑和视线方向；人物应朝向画面内部，不做商业广告摆拍。

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
- 标题重复报错 `checkpoint_verify_miss`/dedupe 时：**更新已有草稿用 `--update-media-id <旧media_id>`**（2026-09-14 用户要求更新而非删除重传）；仅当草稿需要全新独立发布时才删远端 `runs/<run-id>/publish_state.json` 重发。run_id 默认取 meta_path.parent.name（如 newspic），传 `--run-id <日期-slug>` 避免撞历史目录。
- 归档：`/Volumes/外接硬盘/hermes-images/daily-image-training/YYYY-MM-DD-am|pm/`（images/ + orig/ + work/ + README.md + newspic/）。
- 飞书发送最小边 ≥2000 的放大版；MEDIA 路径顶格独立行。

## 风格矩阵速查（写 prompt 用，不再展开）

- 人像：R5 85/1.2 ISO800-1600 窗光/阴天/钨丝灯 · Hasselblad 80/1.9 北窗光 · Leica M11 35/1.4 午后树影
- 风景：Sony 24-70@35 ISO200 三脚架晨光 · Sony 24/1.4 ISO100 蓝调长曝光
- 动物：Sony 400/2.8+1.4x ISO800 金辉轮廓
- 微距：R5 100/2.8 macro ISO400 叶隙晨光
- 建筑：R5 17-40 移轴 ISO100 黄金侧光透视校正 · Sony 16-35/2.8 几何日光 · Leica Q2 28/1.7 晨光纪实
