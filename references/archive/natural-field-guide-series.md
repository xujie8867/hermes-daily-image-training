# Natural Field-Guide Infographic Series

Use when the user likes a soft, comfortable “自然博物图鉴 / observation notes” image and asks for more in the same style.

## Proven style anchor
- Vertical Chinese museum field-guide poster
- cream paper background
- natural science engraving / botanical field-guide illustration
- modern infographic layout
- exactly 6 realistic specimens in the center
- numbered thin-line labels
- subtle ecology background related to the subject
- right-side white info box with a colored border
- bottom poetic one-line slogan
- Chinese text clear, no watermark
- `Style: botanical field-guide infographic`

## Prompt formula
```text
竖版中文博物图鉴海报，主题“{地域/生态位}·{主体}观察笔记”。自然科学版画+现代信息图，cream paper。中央6种写实{主体类别}标本：{标本1} {标本2} {标本3} {标本4} {标本5} {标本6}，带编号细线标注；背景淡淡{生态背景}。顶部标题“{地域/生态位}·{主体}观察笔记”，副标题“{短副标题}”。右侧白底{颜色}边信息框：{信息项1}/{信息项2}/{信息项3}/{信息项4}。底部“{诗意金句}”。中文清晰，无水印。Style: botanical field-guide infographic
```

## Successful extensions from 2026-06-16
1. 青藏高原·野花观察笔记 — 绿绒蒿/雪莲/龙胆花/报春花/点地梅/紫菀；雪山草甸；蓝边信息框。
2. 岭南·草药观察笔记 — 艾草/薄荷/金银花/鱼腥草/益母草/鸡骨草；岭南庭院；绿边信息框。
3. 潮间带·贝壳观察笔记 — 扇贝/牡蛎/蛤蜊/海螺/贻贝/宝贝螺；礁石潮水海藻；蓝边信息框。
4. 热带雨林·蝴蝶观察笔记 — 凤蝶/斑蝶/闪蝶/眼蝶/粉蝶/蛱蝶；雨林叶片雾气；橙边信息框。
5. 河谷湿地·水鸟观察笔记 — 白鹭/苍鹭/鸳鸯/黑水鸡/翠鸟/斑嘴鸭；芦苇浅水晨雾；青边信息框。

## Workflow
1. Reuse the exact style anchor; change only the ecology/subject/specimens/text.
2. Generate sequentially with `image_generate`, not in parallel.
3. Save to a subdirectory under the day folder, e.g. `natural-field-guide-series/`.
4. Make a contact sheet for quick comparison.
5. Run visual check on the contact sheet: verify shared style, subject accuracy, no obvious broken image/watermark/severe garbling.
6. Return the contact sheet first, then each individual `MEDIA:` path.

## Pitfalls
- Do not overload the image with 12+ specimens; 6 is the sweet spot for legibility and specimen detail.
- Keep the prompt around the known safe range for gpt-image-2; do not turn it into a long essay.
- The user’s “舒服” signal here means: soft cream paper, calm colors, organized specimen layout, knowledge-card feel — preserve those, not just the topic.