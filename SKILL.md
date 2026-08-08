---
name: daily-image-training
description: "Load when the user requests image generation, image editing, or image-to-video. Auto-builds structured prompts using the five-segment template, selects generation channels, produces 4 variants, and iterates based on user feedback."
version: "5.0.0"
last_updated: "2026-08-05"
---

# 每日生图 v5 — 新闻摄影写法

## 核心公式（2026-08-05 验证成功）

```
[场景+人物] + [自然光线] + [相机+镜头+ISO] + [皮肤细节] + [纪实风格声明]
→ 禁止：艺术大师名、电影感、舞台调度、cinematic/staged/editorial
```

**为什么**：Crewdson/Salgado/McCurry 等大师名 + "cinematic staging" 在 AI 手里不是摄影参考，是过度风格化指令，出来就是摆拍感/塑料感。换成"Canon EOS R5, 85mm f/1.2, ISO 800, photojournalism candid"效果立竿见影。

## 生图流程

1. **选题**：5个完全不同方向（人像/街头/自然/纪实/建筑），与近7天零重叠，其中至少1张世界有名建筑
2. **写 prompt**：按核心公式，不用任何艺术大师名
3. **生成**：image_generate(portrait)，可并行出5张
4. **归档**：保存到 YYYY-MM-DD-am/ 或 -pm/
5. **报告**：最终响应必须用 `MEDIA:/绝对路径/xxx_2K.png` 逐行列出图片（每张一行），**禁止只写文件路径文本**（2026-08-07 教训：下午场只发了文字路径，用户没收到图）

## 风格矩阵（9种，全部验证通过 · 2026-08-05）

### 人像/人物
| # | 风格 | 镜头+ISO | 光线语法 | 类别 |
|---|------|---------|---------|------|
| 1 | 新闻纪实 | R5 85/1.2, ISO 800-1600 | window light, overcast, tungsten bulb | portrait |
| 2 | 商业时装 | Hasselblad 80/1.9, ISO 100 | north-facing window, indirect daylight | fashion |
| 3 | 旅行人文 | Leica M11 35/1.4, ISO 400-800 | afternoon sun through leaves/dust | travel |
| 6 | 棚拍肖像 | R5 50/1.2, ISO 100 | single softbox 45°, white seamless | studio |
| 5 | 街头快照 | Ricoh GR III 28/2.8, ISO 1600-3200 | mixed city light, no flash | street |

### 自然/动物
| # | 风格 | 镜头+ISO | 光线语法 | 类别 |
|---|------|---------|---------|------|
| 7 | 自然风光 | Sony 24-70/2.8@35, ISO 200, tripod | dawn first light, mist | landscape |
| 8 | 野生动物 | Sony 400/2.8 + 1.4x TC, ISO 800 | rim light, frost, golden hour | wildlife |
| 9 | 昆虫微距 | R5 100/2.8 macro 1:1, ISO 400 | morning filtered through leaf | macro |
| 4 | 极简风光 | Sony 24/1.4, ISO 100, tripod | pre-dawn long exposure 30s | landscape |

### 世界建筑（2026-08-05 新增）
| # | 风格 | 镜头+ISO | 光线语法 | 类别 |
|---|------|---------|---------|------|
| 10 | 经典建筑 | R5 17-40/4 tilt-shift, ISO 100 | late golden light, perspective corrected | architecture |
| 11 | 现代建筑 | Sony 16-35/2.8, ISO 100 | clean daylight, sharp geometry | architecture |
| 12 | 古建纪实 | Leica Q2 28/1.7, ISO 100 | soft morning light, documentary | architecture |

建筑选题：世界著名建筑（故宫/长城/泰姬陵/圣家堂/埃菲尔铁塔/金字塔/帕特农神庙/悉尼歌剧院/圣彼得大教堂/吴哥窟/清水寺/圣托里尼/布拉格城堡），每天1个，AM/PM零重叠。

### 通用负向（人像+动物+微距）
`NOT CGI, NOT 3D render, NOT airbrushed, NOT plastic skin, NOT waxy, NOT doll, NOT beauty filter, NOT over-sharpened, NOT HDR, NOT cinematic lighting, NOT staged, NOT digital art`

### 通用负向（纯风景）
`NOT CGI, NOT 3D render, NOT HDR, NOT over-sharpened, NOT oversaturated, NOT digital art, NOT cinematic`

## 皮肤公式（人像必带）

皮肤：`visible pores + fine vellus hair + natural skin texture + NOT flawless + NOT plastic`
老年皮肤追加：`deep wrinkles + sun-darkened texture + visible capillaries`

## 负向词（每张必带，全量）

```
NOT CGI, NOT 3D render, NOT airbrushed, NOT plastic skin, NOT waxy skin, 
NOT doll-like, NOT beauty filter, NOT over-sharpened, NOT HDR glow, 
NOT cinematic lighting, NOT staged portrait, NOT fashion editorial, 
NOT oversaturated, NOT perfect symmetry
```

## 硬性规则

- **去 AI 感三层（2026-08-07 用户反馈必带）**
  1. **色彩收敛**：prompt 必须写 `muted natural colors, restrained color grading, desaturated shadows, no HDR, no oversaturation`。AI 默认往艳里调，真实照片色彩收敛
  2. **物理真实感层**（人像必带）：`visible skin pores, natural skin texture, subtle imperfections, contact shadows, ambient occlusion, film grain, sensor noise, unretouched`。只写"NOT plastic"不够，要正向注入不完美
  3. **构图去理想化**：`candid, imperfect composition, natural asymmetry, awkward real-world details, no perfect symmetry, no idealized lighting`。AI 最爱"完美"，真实照片有瑕疵
- **锐度铁律**：模型档位决定锐度。gpt-image-2 系列偏软，**Grok(grok-imagine-image-quality) 最锐**。若输出仍偏软 → 重跑换 Grok，不要将就
- **默认通道：relay gpt-image-2（铁律，2026-08-07 起，2026-08-08 用户再次明确）**：所有生图默认一律用 relay 的 gpt-image-2（openai 插件，`image_gen.provider: openai`）。**只有用户主动说「用 grok 试试」「用 gemini 试试」等点名时才切换**，没说就默认 gpt-image-2，禁止自行切换。Gemini 通道（antigravity-gemini 插件）和 Grok 都是"待命备用"，仅用户点名时用，用完切回 openai。
  - 今天 08-07 实测：relay 默认 gpt-image-2 会落到 **medium 档**（缓存文件名 `openai_gpt-image-2-medium_...`），出图软、AI 感重
  - 生图时**显式指定 high 档**：`image_generate(prompt=..., model="gpt-image-2-high")`（若工具不接受 model 参数，则在 prompt 首行写 `high quality, detailed texture, sharp focus`）
  - relay 不可用时的首选替代是 **Grok（grok-imagine-image-quality）**——锐利、AI 感低，比 medium 档更接近用户标准
  - **Gemini 通道（2026-08-08 配置，用户认可质感）**：插件 `antigravity-gemini` → `http://154.217.247.207:8045/v1`，model `gemini-3.1-flash-image`，key `antigravity-2026-8f3a`。`config.yaml` 的 `image_gen.provider: antigravity-gemini` 即启用；改回 `openai` 切回 relay。出图原生 848×1264（需 Lanczos 放大到 2048×3072），~12s，饱和度低（~20）写实感好。⚠️ `gemini-3-pro-image` 系列无配额（502 不可用）。改 `plugins.enabled` 后须 gateway 重启（外部终端）
  - 一切生图先走 relay，禁止默认直连 Codex（429 浪费）
- **Codex 429 历史（2026-08-06）**：Codex OAuth 配额耗尽时 cron 自动按 channel-failure-diagnostics 切换，最终落到 relay gpt-image-2。若 relay 的 gpt-image-2 也失败 → Grok（xai）→ 报告
- 自动切 Grok 场景（仅在 relay 不可用时）：①浅色主体+逆光+浅背景 ②黑白写实特写 ③镜面/反射表面 → 出完切回 relay
- 选题回避：浅色逆光组合、黑白纪实人像、反射表面
- `aspect_ratio=portrait`，prompt 首行写 `Vertical 2:3 portrait, full frame edge to edge`
- 5张=5个不同方向，**人物出现仅限1张（全场铁律）**：5张中只有1张允许出现人物，其余4张必须完全无人物（纯自然/动物/风光/建筑/静物/街道空景），画面内禁止出现人（prompt 明写 no people, empty scene），至少1张世界有名建筑
- **去重铁律（2026-08-08 用户反馈修复）**：选题前必须 `ls /Volumes/外接硬盘/hermes-images/daily-image-training/2026-*/` 列出全部历史产出文件名 + 读各 README 的 style_key，排除历史所有场次已用主题（渔夫/补网/灯塔/雪山等同场景同主体一律视为重复），AM/PM/历史完全不重叠
- **高雅·艺术成分（2026-08-08 用户要求，强制）**：5张整体气质=高雅/艺术感——构图讲究、光线克制、色彩收敛，拒绝平庸糖水片；每张至少命中一个艺术感方向（经典构图/独特光影/名画质感/静谧氛围/手工质感）；艺术手法用相机物理语言写进 prompt（光比/构图/影调），不写艺术大师名；禁止艳俗色彩、网红打卡风、过度饱和、信息图感
- **写实优先（2026-08-08 用户要求，铁律）**：所有图必须是真实可拍到的场景（相机物理语言），拒绝概念艺术/超现实/科幻/梦幻氛围/插画感；每张都要像真实摄影作品（纪实/新闻/国家地理质感，生活化、有细节瑕疵、光线来源合理）；人像那张必须真人感皮肤（毛孔/皱纹/汗珠/红血丝），禁止美颜/柔焦/杂志大片感
- AM/PM 完全不重叠
- Grok 出图必须 curl 下载到本地再 MEDIA 发送；relay（openai 插件）自动存本地缓存

## 放大规则（2026-08-06 验证）

- 用户要求最小边长 ≥2000px、固定 2:3 portrait
- relay gpt-image-2 原生输出 1024×1536（prompt 首行 Vertical 2:3 生效；`size` 参数被忽略）
- ⚠️ Real-ESRGAN 超分脚本（upscale_image.py）**输出坏图**（纯黑，std<20、仅3色），勿用！改用 PIL Lanczos：
  ```python
  from PIL import Image
  im = Image.open(f).convert('RGB')
  im.resize((2048, 3072), Image.LANCZOS).save(f'{f[:-4]}_2K.png', optimize=True)
  ```
- 飞书传输会压缩，发 _2K 版（2048×3072）

## 风格声明词库（prompt 结尾注入）

`Photojournalism, unretouched, candid, raw photo, documentary style, National Geographic`
或 `Photorealistic, unretouched, raw photo, documentary style`
