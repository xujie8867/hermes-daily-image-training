# 超写实生图终极指南 (2026-08-02 全网挖掘)

> 来源：X 社区 × awesome-ai-visual-realism-prompts × 多仓库交叉验证
> 适用：gpt-image-2-high / gpt-image-2-medium

---

## 🎯 核心心法

> *"AI looking AI is a vocabulary problem, not a model problem."*

gpt-image-2 完全有能力出照片级真实图，问题在于提示词缺少物理真实感锚点。以下是从全网挖掘的 10 大技巧。

---

## 1. 三个魔法词

| 词 | 效果 | 来源 |
|---|---|---|
| `photorealistic` | OpenAI 研究员确认在 gpt-image-2 中与旧模型行为不同，单独加就大幅提升真实感 | @jasperdevs |
| `candid` | 打破 AI 的"摆拍感"，注入随机性 | 社区共识 |
| `unretouched` | 禁止 AI 自带的"美颜滤镜" | 高频验证 |

---

## 2. 🚫 避坑：2025-2026 这些词反而让人像变塑料

```
❌ 8K, HDR, hyper detailed, ultra sharp, masterpiece
❌ perfect skin, flawless, beautiful complexion
❌ cinematic bloom, glowing neon, lens flares
```

上列词汇在 2025-2026 模型上会推高"塑料完美感"，尤其 `8K` / `HDR` / `ultra sharp` 是重灾区。

---

## 3. 📷 结构化 Prompt 模板（最终版）

```
[方向] Vertical portrait orientation, 2:3 aspect ratio.
        Subject centered with breathing room, safe for center crop.

[主体] [年龄/描述] [人物/物体] is [做什么] in [环境].

[皮肤] visible pores, realistic microtexture, subsurface scattering,
        fine vellus hair, slight oil sheen on T-zone, subtle freckles,
        NOT flawless, NOT airbrushed, NOT plastic, NOT waxy.

[材质] [布料类型] with visible [织造纹理], natural [褶皱],
        [液体] with Fresnel reflection, surface tension, caustics.

[接触] contact shadow at base, finger compression at grip,
        ambient occlusion, [颜色弹射] from [X] onto [Y].

[表情] Duchenne smile with eye narrowing, subtle facial asymmetry,
        catchlights in both eyes, natural micro-expression.

[布光] [摄影师风格] cinematography: [key方向/角度/硬度/色温],
        [fill], [rim]. Motivated light from [光源来源].

[构图] [构图风格] composition: [framing/机位/主体位置].

[相机] Shot on [相机型号] with [镜头] at f/[光圈],
        [胶片模拟], subtle film grain.

[负向] plastic skin, waxy skin, airbrushed, CGI, 3D render, doll-like,
        oversaturated, HDR, perfect symmetry, frozen expression, dead eyes,
        painted water, floating objects, beauty filter, over-sharpened
```

---

## 4. 🎬 5 位电影摄影师灯光签名（可直接复制）

| DP | 一句话 | 配方 |
|---|---|---|
| **Roger Deakins** | 单光源+深阴影+大气雾 | `single hard key from one side, deep shadow opposite, atmospheric haze, motivated light from window, cool palette with warm practical` |
| **Emmanuel Lubezki** | 全自然光+逆光+金色时刻 | `natural light only, golden hour, strong backlight rimming hair, handheld, warm amber-orange, lens flares, no artificial fill` |
| **Christopher Doyle** | 霓虹+荧光+色温对冲 | `practical lighting only, neon signs, strong color contrast magenta key + cyan fill, tight framing, reflections, smoke` |
| **Darius Khondji** | 钠灯橙+高对比+油腻 | `sodium-vapor orange, heavy practicals, high contrast, deep blacks, greasy surfaces, grain, lived-in` |
| **Hoyte van Hoytema** | IMAX 70mm+冷蓝+暖橙分裂 | `IMAX 70mm, natural light, cold blue ambient + warm orange practical, negative space, photochemical grain, no digital sheen` |

---

## 5. 🖼️ 5 位导演构图签名（可直接复制）

| 导演 | 一句话 | 配方 |
|---|---|---|
| **Kubrick** | 完美对称+单点透视 | `perfect symmetric, one-point perspective, dead center subject, wide angle, eye level, locked-off` |
| **Wes Anderson** | 平面舞台+中心+粉彩 | `flat tableau, subject dead center facing camera, pastel palette, no depth, straight-on` |
| **Wong Kar-wai** | 切边+亲密+倾斜 | `tight cropped, subject bottom third, negative space above, slight dutch tilt, blurred foreground element` |
| **Tarkovsky** | 长镜头+深度+自然元素 | `long take, deep depth, water/fire/smoke in frame, horizon upper third, subject small` |
| **Nolan** | IMAX 宽幅+人小景大 | `IMAX wide, subject small in lower third, vast architecture, strong horizon, clean geometric lines` |

---

## 6. 🎭 皮肤真实感速查

```
正面（必加）:
  visible pores, realistic skin microtexture, subsurface scattering,
  fine vellus hair catching rim light, slight oil sheen on T-zone,
  subtle freckles, natural asymmetry, micro skin variations

年龄适配:
  20-30: "natural youthful skin with subtle texture, dewy finish"
  30-45: "visible fine lines, laugh lines, subtle sun spots"
  45-60: "weathered skin with character lines, deep laugh lines"
  60+:   "deeply textured aged skin, visible wrinkles, natural aging"

禁止:
  flawless skin, perfect skin, glass skin, poreless, airbrushed,
  beauty filter, over-smoothed, retouched, photoshopped
```

---

## 7. 📋 终极负向词库

```
plastic skin, waxy skin, barbie doll, doll-like, airbrushed,
beauty filter, overprocessed, over-sharpened, glossy,
CGI, 3D render, illustration, painting, cartoon, anime,
oversaturated, HDR, glowing neon, cinematic bloom, lens flares,
perfect symmetry, symmetrical face, model pose, dead eyes,
painted water, floating objects, no contact shadows,
deformed hands, extra fingers, fused fingers, bad anatomy,
watermark, text, logo, signature, jpeg artifacts,
blurry, soft focus, low quality, out of frame,
smeared background, blob background, noise foliage,
cloned faces, mirrored elements
```

---

## 8. 🎞️ 胶片模拟速查

| 胶片 | 效果 | 适用 |
|------|------|------|
| Kodak Portra 400 | 暖调肤色，低反差，细颗粒 | 人像/生活 |
| Kodak Portra 800 | 同上+更多颗粒，低光 | 夜景/室内 |
| Fuji Superia 400 | 冷绿调，高饱和 | 街拍/旅行 |
| Kodak Tri-X 400 | 黑白，粗颗粒，高反差 | 纪实/街头 |
| Cinestill 800T | 蓝调高光，霓虹红晕 | 夜景/城市 |

---

## 9. 🏷️ 高级技巧碎片

1. **参考图先行**：上传 Pinterest/真实照片给 Claude 分析色彩→生成 JSON→喂给 gpt-image-2
2. **iPhone 照片感**：`raw iPhone 15 Pro photo, f/1.8, slight grain, candid`
3. **结构化分段**：prompt 用 `[Subject] [Camera] [Light] [Aesthetic] [Constraints]` 分割
4. **细节预算**：焦点区全微纹→中景可读→远景无 blob，不要用模糊掩盖缺失的细节
5. **物体时间状态**：`worn, dusty, fingerprints, edge wear, micro-scratches`
6. **"比背景还重要"的接触**：`contact shadow, ambient occlusion, finger compression`
7. **光线揭示纹理**：`light skims across skin revealing realistic pores and texture`
8. **3×3 光照网格**：同一个人物 9 种光照，一次性测试皮肤一致性

---

## 10. ⚡ 生图前检查清单

```
□ prompt 首行硬编码 "Vertical portrait orientation, 2:3"
□ 有 camera + lens + aperture 三段式
□ 有具体的布光方案（非 "nice lighting"）
□ 有皮肤真实感关键词（非 "beautiful skin"）
□ 有材质物理关键词（fabric weave / Fresnel / SSS）
□ 有接触物理（contact shadow / compression）
□ 有微表情（Duchenne smile / asymmetry / catchlights）
□ 有负向词 ≥10 个（含 plastic skin / CGI / doll-like）
□ 有胶片模拟或风格锚点
□ 生成后用 PIL 验尺寸 → 非竖版则重出
```
