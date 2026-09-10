# 4:3 craft / museum infographic series

Session lesson: user praised the daily traditional-craft cutaway image and asked to change the image ratio to 4:3, then generate 5 more in the same style. This differs from the science editorial 4:3 series: the subject family is traditional craft / non-heritage engineering / museum didactic panels, not ecology or geology.

## Trigger
Use this when the user asks for:
- “今天这张图同款风格，改成4:3” after a craft/cutaway daily image
- traditional Chinese craft / non-heritage / museum-style technical infographic series
- 榫卯、斗拱、活字印刷、造纸、青铜铸造、陶瓷、织机、漆器等工艺结构图

## Format defaults
- Aspect: 4:3 landscape.
- Generate with `image_generate(aspect_ratio="portrait")`, target 1024×1536 (2:3).
- If exact dimensions are needed, normalize to 1600×1200 by padding/resizing, not hard-cropping. Padding preserves title, info boxes, and bottom line.
- Layout: warm museum/paper background; central-left subject as cutaway, exploded diagram, or process line; right-side white info panel with colored border; top title/subtitle; bottom poetic takeaway.
- Style: modern museum infographic + artisan hand-drawn texture + soft 45° light.
- Chinese text should be direct, concise, and specified verbatim.

## Proven prompt formula
```text
横版4:3中文科普海报，主题“{主题}”。暖米色{宣纸/博物馆/纸纹}底，中央偏左是{传统工艺主体}：{5-6个结构/流程部件}，{分层悬浮/剖面流水线/爆炸图}，细线编号。顶部标题“{主题}”，副标题“{一句通俗解释}”。右侧白底{强调色}边信息框：{知识点1}/{知识点2}/{知识点3}/{知识点4}。底部“{诗意总结金句}”。现代博物馆信息图+工匠手绘质感，45°柔光，中文清晰，无水印。
```

## Good topics from this session
- 榫卯木构结构解剖图 — 棕色边；燕尾榫、抱肩榫、穿斗、斗拱、楔钉；信息框：受力互锁/可拆可修/木材呼吸/抗震韧性；底部：木头之间 自有山河。
- 斗拱承重结构解剖图 — 朱棕边；栌斗、华拱、昂、耍头、梁枋；信息框：层层传力/出檐遮雨/榫卯咬合/等级秩序；底部：屋檐之下 藏着古人的工程学。
- 活字印刷机关解剖图 — 墨黑边；字模、字盘、墨辊、版框、压印板、宣纸；信息框：单字复用/排版成页/上墨压印/知识复制；底部：一个字的移动 改变了书的速度。
- 古法造纸流程解剖图 — 青绿边；蒸煮纤维、舂捣纸浆、竹帘抄纸、压榨、晾晒；信息框：纤维分散/竹帘成形/压榨脱水/日光干燥；底部：薄薄一页 托住千年文字。
- 青铜器失蜡铸造解剖图 — 青铜绿边；蜡模、泥范、浇口、铜液、冷却脱范、纹饰打磨；信息框：蜡模塑形/泥范包裹/高温浇铸/纹饰成型；底部：火把礼器 从泥土里唤醒。

## Verification checklist
- Confirm exact 4:3 output dimensions when requested, preferably 1600×1200.
- Verify visually via a contact sheet before reporting: title, subtitle, main diagram, right info panel, and bottom line are not cropped.
- Save semantic filenames under the day directory, plus `metadata.json` and README with prompts/dimensions.
- Send all finished images as `MEDIA:` links, and optionally include the contact sheet so the user can compare quickly.
