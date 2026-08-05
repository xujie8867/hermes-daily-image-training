# GPT-Image-2 锐利摄影 Prompt 精华（2026 社区挖掘）

> 来源：X/Twitter 社区 2026 年高质量 post，非现有提示词库。
> 这些 prompt 的共性：镜头参数 + 皮肤纹理 + 负向词 + 权威锚点 = 不糊。

## 核心锐利公式

```
[相机+镜头] [主体+表情] [光照] [锐利词堆叠] [皮肤微观纹理] [构图] [权威锚] [负向词]
```

## 锐利关键词清单

### 正面（必加）
- `tack-sharp focus`, `razor-sharp detail`, `maximum sharpness`, `maximum acuity`
- `crystal clear iris details`, `sharp focus locked on the eyes`
- `ultra-detailed skin texture`, `visible pores`, `skin micro-texture`
- `high micro-contrast`, `crisp edge definition`, `intricate details`
- `hyper-realistic`, `photorealistic DSLR quality`, `8K resolution`, `32K`

### 负向词（每个 prompt 必带）
```
blurry, motion blur, out of focus, soft focus, defocus, blurry eyes,
oversmoothed skin, plastic skin, waxy skin, low resolution, AI artifacts,
deformed, low quality, hazy, foggy
```

### 相机锚点（选一个）
- `Canon EOS R5` — 通用专业
- `Sony A1 / Sony A9 III` — 高锐度
- `Hasselblad H6D-100c` — 商业级
- `Leica SL2-S / Leica M11` — 纪实/艺术
- `Phase One XF IQ4` — 影棚顶配

### 镜头公式
- 人像：`85mm f/1.8` 或 `85mm f/1.4`
- 风景：`24mm f/8` 或 `50mm f/11`
- 街拍：`35mm f/2.8` 或 `50mm f/1.4`
- 微距：`100mm f/2.8 macro`

### 权威锚点
- 人像：`National Geographic portrait style`, `Vogue editorial`, `Vogue Italia`
- 风景：`National Geographic cover aesthetic`, `Condé Nast Traveler`
- 电影感：`Kodak Portra 400`, `Annie Leibovitz`

## 经典 Prompt 模板

### 模板1：工作室人像（干净高级）
```
Ultra-realistic close-up studio portrait of [人物描述], razor-sharp focus on eyes
with perfect catchlight, tack sharp eyelashes and iris details, ultra-detailed skin
with visible pores and natural texture, [造型描述]. Soft diffused key lighting +
gentle rim light, clean [颜色] seamless background. Shot on [相机] with [镜头],
maximum sharpness and acuity, high micro-contrast, [权威锚], [分辨率], photorealistic.

Negative: blurry, motion blur, soft focus, oversmoothed skin, plastic skin, low quality,
AI artifacts, hazy, deformed
```

### 模板2：自然光人像（日系清新）
```
Photorealistic natural light portrait of [人物描述], razor sharp focus on eyes,
extremely detailed skin texture and pores, soft window light from the side creating
gentle shadows. Shot on 85mm f/1.8 lens, crisp image, high acuity, individual hair
strands visible, clean and sharp, [风格], 8K, ultra detailed, natural skin, no blur.

Negative: blurry, soft focus, oversmoothed, plastic skin, low resolution, motion blur
```

### 模板3：街拍人像（蓝调时刻）
```
Ultra-photorealistic cinematic street portrait on a bustling city street at blue hour.
[人物描述], shot through glass creating layered reflections. Long-exposure traffic light
trails in vibrant colors, soft neon bokeh. Mixed twilight and storefront lighting with
gentle rim light. Razor-sharp focus on eyes, fabric texture, and skin pores, shallow
depth of field. Leica SL2-S with Summilux 50mm f/1.4, Kodak Portra 400 palette,
ultra-sharp details, Vogue street editorial, 8K HDR.

Negative: blurry, motion blur, soft focus, oversmoothed skin, plastic skin
```

### 模板4：风景（国家地理级）
```
Ultra-photorealistic landscape photography of [地点] at golden hour. [景观描述]
with razor-sharp detail and crisp edge definition. Volumetric god rays, rich natural
color palette. Shot on Sony A1 with 24mm f/8 lens, f/11 aperture, hyper-detailed
textures, National Geographic cover aesthetic, 8K HDR, impeccable clarity.

Negative: blurry, soft focus, low resolution, hazy, AI artifacts
```

### 模板5：时尚编辑（杂志大片）
```
Ultra-detailed hyperrealistic 8K cinematic fashion portrait of [人物描述].
[服饰描述]. Dramatic side lighting and soft fill creating crisp highlights on
fabric folds and razor-sharp texture details. Perfect skin texture, individual hair
strands, and garment stitching all ultra-crisp. Shot on Hasselblad H6D with 100mm
f/2.8 lens, shallow depth of field with tack-sharp focus on eyes, Vogue editorial,
impeccable clarity.

Negative: blurry, oversmoothed skin, plastic skin, motion blur, low quality
```

## 实战口诀

1. **镜头必有光圈** — `85mm f/1.8` 不是 `85mm lens`
2. **皮肤要毛孔不要光滑** — `visible pores, skin micro-texture`
3. **每张带负向词** — `blurry, oversmoothed skin, plastic skin`
4. **挂权威锚点** — `National Geographic` / `Vogue` 强烈暗示高画质
5. **prompt < 250 字** — gpt-image-2-high 安全上限
