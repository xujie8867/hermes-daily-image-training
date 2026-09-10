# 4:3 science editorial infographic series

Session lesson: user liked the random daily science infographic style and asked for the same style in 4:3, then five more matching images.

## Trigger
Use this when the user asks for:
- “同款风格” after a daily random science image
- 4:3 横版科普图 / science infographic series
- A batch of ecosystem / geology / biology / climate science posters

## Format defaults
- Aspect: 4:3 landscape.
- Generate via `image_generate(aspect_ratio="portrait")`, target 1024×1536 (2:3).
- Layout: left/center visual scene + right-side white info panel + top title/subtitle + bottom poetic one-line takeaway.
- Style: modern science editorial infographic + documentary texture.
- Chinese text must be specified directly and kept concise.

## Proven prompt formula
```text
横版4:3中文科普海报，主题“{主题}”。{主色环境背景}，中央偏左是{核心科学主体/剖面/场景}，周围有{3-6个关键细节或生物/结构}。顶部标题“{主题}”，副标题“{一句通俗科学解释}”。右侧白底{强调色}边信息框：{知识点1}/{知识点2}/{知识点3}/{知识点4}。底部“{诗意总结金句}”。现代科学插画+纪录片质感，{主色}+{强调色}，中文清晰，无水印。
```

## Good topic patterns from this session
- 深海热液喷口生命图谱 — 冷蓝+硫磺橙；黑烟囱、管虫、盲虾、贻贝；信息框：化能合成/高温矿物/共生微生物/深海生态。
- 亚马逊雨林菌根网络图谱 — 深绿+暖金；巨树剖面、发光菌丝；信息框：菌根共生/碳水交换/营养传递/森林互助。
- 南极冰下湖生命图谱 — 冰蓝+银白；厚冰层剖面、暗色冰下湖、钻孔；信息框：极端低温/无光环境/微生物代谢/冰芯探测。
- 撒哈拉夜行生命图谱 — 沙金+夜蓝；沙丘剖面、夜行动物、地下洞穴；信息框：昼伏夜出/节水结构/沙下洞穴/热量调节。
- 珊瑚白化警报图谱 — 海蓝+珊瑚橙；健康/白化珊瑚对比；信息框：共生藻/热压力/颜色褪去/生态连锁。
- 火山岛诞生图谱 — 熔岩橙+海蓝；海底火山剖面、新生岛；信息框：板块运动/岩浆上涌/熔岩冷却/生态登陆。

## Verification checklist
- Confirm exact 4:3 output dimensions if user requested 4:3 (e.g. `1600×1200`).
- Visually verify: title, subtitle, right info panel, main subject, bottom line are complete and not cropped.
- Save each image with semantic filename and store a README with the prompt and dimensions.
- For batches, send all images back as `MEDIA:` links after verification.
