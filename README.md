# Hermes 每日生图训练

> AI 生成的照片，要像照片——不是 AI 画。

一套经过实战验证的 AI 生图提示词方法论。**9 种风格，9 投 9 中。** 基于 [Hermes Agent](https://hermes-agent.nousresearch.com) + OpenAI Codex (gpt-image-2-high) + xAI Grok。

[English version below](#english)

---

## 问题

我们收藏了 721 条精选 prompt、348 条专业摄影参考、全套摄影大师技巧。**知识越多，图越差。**

| 以前的写法 | 结果 |
|---|---|
| "Gregory Crewdson 电影感舞台调度" | 塑料感、摆拍、AI 味 |
| "Rembrandt 三角光 + Kodak Portra 400" | 糊片、假、找不到感觉 |
| "Sebastião Salgado 力量纪实" | 皮肤假、太假、恐怖谷 |

## 发现

**AI 不理解艺术史——它理解相机物理。**

你说"Annie Leibovitz 戏剧性肖像"，模型画的是「一幅 Leibovitz 风格的作品」——经过风格化、二手诠释。

你说"Canon EOS R5, 85mm f/1.2, ISO 800, 单灯柔光箱 45°"，模型渲染的是物理约束：f/1.2 的浅景深、ISO 800 的干净噪点、45° 柔光箱的单侧软阴影。

**不要给 AI 当艺术指导。给它租一支镜头。**

---

## 核心公式

```
[ 场景+人物 ] + [ 自然光线 ] + [ 相机+镜头+ISO ] + [ 皮肤/纹理细节 ] + [ 纪实风格声明 ]

⛔ 永不用：摄影师名字、cinematic、editorial、staged、胶片型号
✅ 必须写：相机型号、焦段、光圈、ISO、自然光描述
```

## 三层分离架构

```
┌─────────────────────────────────────────┐
│ 第一层：生成 prompt（给 AI 看，≤150 字）  │
│ 场景+光线+相机+皮肤+负向词                │
│ ⛔ 不含大师名、胶片名、电影感              │
├─────────────────────────────────────────┤
│ 第二层：知识库（Agent 自己看）             │
│ 721条prompt、拉鲁斯348、大师技巧全集       │
│ → Agent 翻译成第一层语言再写入 prompt      │
├─────────────────────────────────────────┤
│ 第三层：负向词（给 AI 看）                 │
│ 只告诉 AI「不要什么」，不管它「怎么做」     │
└─────────────────────────────────────────┘
```

**721 条 prompt 不是指令——是灵感。** Agent 从中选题、构图，翻译成镜头参数语言喂给模型。

---

## 9 种已验证风格

2026-08-05 全天验证，全部一次出图，零重试。

### 人像/人物

| # | 风格 | 镜头+ISO | 光线 | 适用 |
|---|------|---------|------|------|
| 1 | 新闻纪实 | R5 85/1.2, ISO 800-1600 | 窗光、阴天、钨丝灯 | 街拍、纪录、写实 |
| 2 | 商业时装 | Hasselblad 80/1.9, ISO 100 | 北向窗、间接日光 | 干净高级、产品+模特 |
| 3 | 旅行人文 | Leica M11 35/1.4, ISO 400-800 | 午后阳光透树叶 | 国家地理感 |
| 5 | 街头快照 | Ricoh GR III 28/2.8, ISO 1600-3200 | 城市混合光、无闪 | 粗粝真实、森山味 |
| 6 | 棚拍肖像 | R5 50/1.2, ISO 100 | 单灯柔光箱 45°、白背景 | 专业头像 |

### 自然/动物

| # | 风格 | 镜头+ISO | 光线 | 适用 |
|---|------|---------|------|------|
| 4 | 极简风光 | Sony 24/1.4, ISO 100, 三脚架 | 黎明前长曝光 30s | 静谧大气 |
| 7 | 自然风光 | Sony 24-70/2.8@35, ISO 200 | 晨雾、第一缕光 | 山水、大景 |
| 8 | 野生动物 | Sony 400/2.8 + 1.4x TC, ISO 800 | 轮廓光、霜原、金色时刻 | 动物栖息 |
| 9 | 昆虫微距 | R5 100/2.8 macro 1:1, ISO 400 | 晨光透叶片 | 极致特写 |

### 图例

| 新闻纪实 | 野生动物 | 微距 |
|---|---|---|
| ![胡同](examples/01-photojournalism-hutong.jpg) | ![赤狐](examples/02-wildlife-fox.jpg) | ![螳螂](examples/03-macro-mantis.jpg) |

| 旅行人文 | 自然风光 |
|---|---|
| ![地中海](examples/04-travel-mediterranean.jpg) | ![桂林](examples/05-landscape-guilin.jpg) |

---

## 负向词

### 人像/动物/微距
```
NOT CGI, 3D render, airbrushed, plastic skin, waxy, doll-like,
beauty filter, over-sharpened, HDR glow, cinematic lighting,
staged portrait, fashion editorial, digital art
```

### 纯风景
```
NOT CGI, 3D render, HDR, over-sharpened, oversaturated,
digital art, cinematic
```

---

## 自动切换规则

默认 Codex (gpt-image-2-high)，以下场景立即切 Grok：

1. 浅色主体 + 逆光 + 浅色背景（必糊）
2. 黑白写实人像（AI 面部先天失真）
3. 镜面/反射表面（盐沼、水面、玻璃）

出完切回 Codex。

---

## 关键踩坑

- `aspect_ratio` 参数不可靠 → prompt 首行写比例
- prompt 超 250 字容易空响应 → 精简
- 飞书压缩吃掉低反差画面锐度 → 深背景 + 硬光起步
- Grok 出图必须 curl 下载到本地再发，不用 x.ai CDN 链接

---

## 版本

| 版本 | 日期 | 变更 |
|------|------|------|
| v5.1.1 | 2026-08-05 | 专业 README + 示例图 |
| v5.1.0 | 2026-08-05 | 9 风格完整矩阵，全部验证通过 |
| v5.0.0 | 2026-08-05 | 新闻摄影写法：弃艺术大师名，用镜头参数 |
| v4.0.0 | 2026-08-04 | 艺术感 v2.0 框架（已被 v5 取代） |

---

## English

### The Core Insight

After accumulating 721 curated prompts and professional photography knowledge, our AI images got **worse**. Why?

**AI models don't understand art history — they understand camera physics.**

| Art Reference Approach | Camera Physics Approach |
|---|---|
| "Gregory Crewdson cinematic staging" | "Canon EOS R5, 85mm f/1.2, ISO 800, blue hour twilight" |
| → Stylized, plastic, AI-feeling | → Photorealistic, natural |

The fix: describe the scene in terms of physical constraints — lens, aperture, ISO, natural light — rather than artistic movements or photographer names.

### The Formula

```
[ Scene + Subject ] + [ Natural Light ] + [ Camera + Lens + ISO ] + [ Texture Detail ] + [ Documentary Style Claim ]

⛔ NEVER: photographer names, "cinematic", "editorial", film stocks
✅ ALWAYS: camera model, focal length, aperture, ISO, natural light
```

### Three-Layer Architecture

- **Layer 1**: Generation prompt (for the model, ≤150 words) — scene + light + camera + skin + negatives
- **Layer 2**: Knowledge base (Agent only) — 721 prompts, photography references → Agent translates into Layer 1
- **Layer 3**: Negative keywords — tell AI what NOT to do, never how to do it

All 9 styles (portrait, fashion, travel, street, studio, landscape, wildlife, macro, minimalist) verified in a single day with zero retries.

---

Built for [Hermes Agent](https://hermes-agent.nousresearch.com) by Nous Research.  
Methodology discovered through iterative testing on 2026-08-05.
