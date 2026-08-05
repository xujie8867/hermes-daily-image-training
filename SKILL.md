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

1. **选题**：4个完全不同方向（人像/街头/自然/纪实），与近7天零重叠
2. **写 prompt**：按核心公式，不用任何艺术大师名
3. **生成**：image_generate(portrait)，可并行出4张
4. **归档**：保存到 YYYY-MM-DD-am/ 或 -pm/
5. **报告**：MEDIA 发图

## 可用资源（prompt 注入参考，不暴露给 AI）

### 自然光线方案
`overcast soft daylight` / `foggy morning diffused` / `blue hour twilight` / `golden hour warm ambient` / `window light natural side` / `single warm practical bulb`

### 相机+镜头+ISO（必须写到 prompt 里）
`Canon EOS R5 + 85mm f/1.2, ISO 800-1600` / `Sony A7R V + 50mm f/1.4, ISO 400-1600` / `Leica M11 + 35mm f/1.4, ISO 1600-3200` / `Sony A7R V + 70-200mm f/2.8, ISO 400`

### 构图
`rule of thirds` / `leading lines` / `negative space` / `asymmetrical balance` / `foreground bokeh depth`

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

- 默认 Codex（gpt-image-2-high）
- 自动切 Grok 场景：①浅色主体+逆光+浅背景 ②黑白写实特写 ③镜面/反射表面 → 出完切回 Codex
- 选题回避：浅色逆光组合、黑白纪实人像、反射表面
- `aspect_ratio=portrait`，prompt 首行写 `Vertical 2:3 portrait, full frame edge to edge`
- 4张=4个不同方向，有2张带人物
- AM/PM 完全不重叠
- Grok 出图必须 curl 下载到本地再 MEDIA 发送

## 风格声明词库（prompt 结尾注入）

`Photojournalism, unretouched, candid, raw photo, documentary style, National Geographic`
或 `Photorealistic, unretouched, raw photo, documentary style`
