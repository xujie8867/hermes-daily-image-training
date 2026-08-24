---
name: daily-image-training
description: "Load when the user requests image generation, image editing, or image-to-video. Auto-builds structured prompts using the five-segment template, selects generation channels, produces 4 variants, and iterates based on user feedback."
version: "5.4.0"
last_updated: "2026-08-24"
---

# 每日生图 v5 — 新闻摄影写法

## 🚨 第一优先·交付铁律（2026-08-10 强化——连续漏发，必须最先做）

1. **最后一步 = 发图，不可省略**。生成完 5 张 _2K.png 后先 `ls -la` 确认文件存在
2. **最终响应必须逐行列出 5 个 MEDIA: 路径**（`MEDIA:/绝对路径/xxx_2K.png`，每行一个）
3. 只写文字总结=白生成！用户看不到外接硬盘，不带 MEDIA 图片就到不了用户手里
4. 失败/缺图必须报告，不静默

> ⚠️ 08-09/08-10 连续漏发根因：prompt 膨胀到 5K+ 字符后 deepseek-v4-flash 忽略尾部交付指令。**交付铁律必须放在 prompt/skill 最顶部**（cron prompt 已置顶 2026-08-10）。后续加新规则时不要把它挤下去。

## 📚 提示词库选题（2026-08-10 用户要求，强制优先）

- **题库位置**：`/Volumes/外接硬盘/hermes-images/daily-image-training/resources/awesome-gpt-image2/all-prompts.json`（894条：landscape 171 / portrait 155 / photography-miraivfx 98 / illustration-miraivfx 40 / wildlife 27 / street 21 / artistic-photography 25 / image-generation 347 / 未分类 10）
- **选题流程**：每张先按分类从题库随机抽候选（python `random.sample` 抽 5-8 条 → 挑最符合的 1 条），其标题+核心意象=本张主题方向；分类对应：人像→portrait、风景→landscape、动物→wildlife、街拍→street、艺术感→artistic-photography/photography-miraivfx
- **去重照旧**：题库抽到的主题仍过 .am-themes.json + 近7天历史去重（标题/意象重复重抽）
- 题库只作主题灵感，最终 prompt 仍按 v5 公式重写（相机物理语言 + female-portrait-director）

## 核心公式（2026-08-05 验证成功）

```
[场景+人物] + [自然光线] + [相机+镜头+ISO] + [皮肤细节] + [纪实风格声明]
→ 禁止：艺术大师名、电影感、舞台调度、cinematic/staged/editorial
```

**为什么**：Crewdson/Salgado/McCurry 等大师名 + "cinematic staging" 在 AI 手里不是摄影参考，是过度风格化指令，出来就是摆拍感/塑料感。换成"Canon EOS R5, 85mm f/1.2, ISO 800, photojournalism candid"效果立竿见影。

## 生图流程

1. **选题（方向骨架随机化 · 2026-08-15 用户要求）**：
   - **不再固定 5 类配额**！每天从"方向池"随机抽骨架，避免每天都看起来是同一类（旧规则：人像+建筑+野生动物+意境风景+静物 固定组合 → 感觉重复）
   - **铁律保留（每天必有）**：①1 张女性人像（唯一带人物）②至少 1 张世界著名建筑 ③至少 1 张有意境风景
   - **自由 2 张**：从方向池随机抽 2 个（每场不同，避免与历史场次重复）
   - **方向池**（每张从不同方向选，与近 7 天零重叠）：野生动物 / 昆虫微距 / 街头纪实 / 新闻摄影 / 工业场景 / 天文观测 / 民俗节庆 / 宗教空间 / 老物件静物 / 植物图鉴 / 水下摄影 / 极简航拍 / 体育竞技 / 市井美食 / 废墟遗迹 / 港口渔市 / 山地徒步 / 沙漠戈壁 / 雨林植物 / 雪域高原 / 极地风光 / 都市夜景
   - **骨架去重**：7 天窗口内，同样的"方向组合"不重复出现（如今天 [人像+建筑+风景+野生动物+静物]，明天骨架必须不同，可 [人像+建筑+风景+街头+工业]）
   - **题材池 shuffle**：每次运行先洗牌再挑选，5 张方向+风格各不相同
2. **写 prompt**：按核心公式，不用任何艺术大师名
3. **生成**：image_generate(portrait)，可并行出5张
4. **归档**：保存到 YYYY-MM-DD-am/ 或 -pm/
5. **报告（交付铁律，2026-08-07 + 2026-08-10 强化）**：最终响应**必须**用 `MEDIA:/绝对路径/xxx_2K.png` 逐行列出 5 张图（每张一行）。**先 `ls -la` 确认 _2K 文件真实存在，再把实际路径逐行写进 MEDIA**。禁止只写文字总结/路径文本——用户看不到外接硬盘，不带 MEDIA 就等于白生成（08-09/08-10 连续漏发教训）。失败要报告原因，不静默

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

- **高级艺术感配额（2026-08-09 用户反馈修复，强制）**：每日 5 张中至少 3 张必须是**高级艺术感主题/构图**（参考已验证惊艳的 MiraiVFX 方向），不再每天"手艺人+窗光"稳妥纪实：
  - 高冲击题材池（每张从不同方向选，与近 7 天零重叠）：雨夜霓虹反射街头、直闪胶片人像（黑色背景+硬闪光+复古胶片）、极简航拍、雕版插画质感、植物图鉴/博物画、翡翠微缩/器物微缩、强光比剪影、极端天气（风暴/极光/浓雾）、决定性瞬间、青橙分色夜景
  - 构图艺术感：黄金分割/负空间留白/几何秩序/框架构图/低角度仰视/俯视航拍
  - 光影艺术感：硬光比（伦勃朗/蝴蝶光）、逆光轮廓、霓虹分色（teal shadows + warm highlights）、单束光束、发丝光（hair light 深发深背景分离）、光束透过源+haze（god rays through window/foliage，避免 AI 乱画角度）、彩色bokeh（背景灯源圆斑）
  - **光线闭环+材质响应（2026-08-23 周更）**：每张写清 `光源 + 方向/角度 + 软硬 + 衰减/补光`；涉及布料/金属/玻璃时再写光如何作用于材质（织纹、透光、窄高光、反射），不只写 `detailed texture`
  - 仍限"真实可拍"：不超现实/科幻/梦幻，只是题材和光影更有张力；色彩锚点每张至少一个（暖光斑/彩色主体/金色时刻），禁止全图灰调
- **有意境风景主题（2026-08-09 用户要求，强制）**：每日 5 张中至少 1 张必须是有意境的风景（poetic landscape），优先从自然/极简风光里出：
  - 意境方向（每张不同，与近7天零重叠）：薄雾孤舟/晨雾山峦 · 蓝调时刻旷野 · 孤树于旷野(极简留白) · 云雾海/云上日出 · 雨后湿润空镜 · 雪后静谧 · 长曝光雾化流水 · 芦苇荡夕照 · 水墨意境山峦(真实可拍非插画)
  - 构图语法：极简负空间留白 · 单一主体居中/偏黄金分割 · 大片天空或雾面留白 · 地平线压到 1/3 或 2/3
  - 光影语法：薄雾柔光 · 蓝调时刻(blue hour) · 微弱暖色天光 · 逆光剪影山脊(仅轮廓，避免浅色+逆光坏图组合)
  - prompt 相机物理语言：`mist, fog, blue hour, negative space, lone tree, long exposure, soft diffused light, minimal composition` + 相机(Sony 24/1.4, ISO 100, tripod 30s)
  - 仍限真实可拍；色彩锚点=微弱暖色天光/晨雾金光，禁止全图死灰
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
- **人像=女性（2026-08-10 用户要求，铁律）**：带人物那张一律**女性人像**（禁止男性/老人/小孩）；必须用 female-portrait-director 技能执导——先 skill_view(name='female-portrait-director') 按其 5 段式规范展开（人物设定/时间与动作/身形线条与服饰/场景构图与镜头/布光滤镜），输出模式=直接生成图片；风格池（20 种中选，每张不同）：低饱和电影感/直闪胶片/CCD氛围/极简studio/旅行生活感等，配合相机物理语言（相机+镜头+ISO+布光）
- **去重铁律（2026-08-08 用户反馈修复 + 2026-08-10 强化 + 2026-08-11 光影模板去重）**：选题前必须 `ls /Volumes/外接硬盘/hermes-images/daily-image-training/2026-*/` 列出全部历史产出文件名 + 读各 README 的 style_key，排除历史所有场次已用主题（渔夫/补网/灯塔/雪山等同场景同主体一律视为重复），AM/PM/历史完全不重叠
  - **光影/氛围模板去重（2026-08-11 用户反馈：下午场"清水寺晨雾/瀑布长曝光/红鹿晨雾金辉"与近7天重复后已替换为圣索菲亚黄昏侧光/雪后孤仓/蜂鸟逆光微距，三张获「很好」）**：题库随机抽题时同类光影模板命中率过高。以下光影/氛围关键词 7 天内每种最多用 1 次，抽到重复即重抽：
    - 晨雾（mist/dawn mist，如雪鸮晨雾/老虎晨雾/红鹿晨雾/清水寺晨雾/城堡晨雾）
    - 金辉轮廓（golden rim light 动物类，如雪狼金辉/红鹿金辉）
    - 长曝光雾化流水（long exposure water，十二门徒/瀑布）
    - 黄金时刻建筑（golden hour architecture，泰姬陵/帕特农/圣家堂/斗兽场）
    - 雪景静谧（snow quiet scene）
    - 蓝调时刻（blue hour）
    - 单束光束暗房（single light beam）
  - **弃套路换光线思路（2026-08-11 验证有效）**：某配额（建筑/风景/动物）历史反复出现同套路时，**保持主体配额不变，只换光线/氛围维度**——如建筑弃"晨雾"改"黄昏侧光+动态元素(鸽群)"、风景弃"长曝光"改"雪后静谧负空间"、动物弃"晨雾金辉"改"高速定格+逆光微距"。主体不重复且光线维度也不重复
- **AM/PM 双维度互斥（2026-08-10 用户强调）**：上午场出完必须把 [主题+风格] 写入 `.am-themes.json`（覆盖式）；下午场开跑前先读 `.am-themes.json`，今天上午出现过的主题和风格下午一律禁止；主题、风格、场景三维度都不得与近7天重复
- **打乱（2026-08-10 用户要求）**：候选题材池/风格矩阵每次运行先随机洗牌（shuffle）再挑选，禁止固定顺序；5张主题方向+风格各不相同
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
