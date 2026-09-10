# Educational Cutaway Infrastructure Series

Use this reference when the user asks for “同款风格” after a city infrastructure / engineering-system cutaway infographic, or when daily-image-training needs a new non-repeating high-density science illustration direction.

## Trigger

- 用户喜欢“海绵城市暴雨系统剖面图”这类图。
- 用户说“同款风格再来几张不同案例”。
- 每日生图需要避开美食地图、城市海报、文博微缩、文博材料图鉴等近期主题。

## Visual formula

**Class:** 竖版中文科普剖面海报 / educational-cutaway infographic

**Core structure:**
1. 地上/地面层：真实城市或设施外观，有人物/车辆/建筑作为尺度参照。
2. 地下/内部剖面：展示系统组件和流向。
3. 顶部：中文大标题 + 一句副标题。
4. 12 个编号标注圈 + 每个短说明，编号必须写死。
5. 四角信息面板：知识贴士 / 问题引导 / 小工程师或小角色 / 系统档案。
6. 底部流程条：A→B→C→D→E。
7. 配色：深蓝 + 亮橙 + 白；现代写实 + 儿童科普绘本质感。
8. 约束：中文清晰，无乱码，无水印。

## Known-good base prompt

```text
竖版中文科普剖面海报，主题“{系统名称}”。画面是{系统剖面描述}：地上有{地上元素}；地下/内部展示{8-12个关键组件}。顶部标题“{系统名称}”，副标题“{一句好懂的解释}”。12个编号标注圈+短说明，四角信息面板：知识贴士/问题引导/{小角色}/系统档案。底部流程“{步骤1}→{步骤2}→{步骤3}→{步骤4}→{步骤5}”。现代写实+儿童科普绘本质感，深蓝+亮橙+白，中文清晰，无乱码，无水印。Style: educational-cutaway infographic
```

Keep the prompt concise; long dense Chinese prompts can still work with gpt-image-2, but for reliability prefer ~220-320 Chinese characters and avoid overloading every component with long explanatory text.

## Validated examples from 2026-06-14

### 1. 海绵城市暴雨系统

```text
竖版中文科普剖面海报，主题“海绵城市暴雨系统”。画面是现代城市街区地下剖面：地上有雨中行人、树池、公交站、透水铺装；地下展示雨水花园、渗透井、蓄水模块、排水管网、调蓄池、回用泵。顶部标题“海绵城市暴雨系统”，副标题“让一场大雨被城市慢慢吸收”。12个编号标注圈+短说明，四角信息面板：知识贴士/问题引导/小工程师/城市档案。底部流程“降雨→渗透→储存→净化→回用”。现代写实+儿童科普绘本质感，深蓝+亮橙+白，中文清晰，无乱码，无水印。Style: educational-cutaway infographic
```

### 2. 地铁站通风系统

```text
竖版中文科普剖面海报，主题“地铁站通风系统”。画面是现代地铁站地下剖面：地上有城市道路、出入口、风亭；地下展示站厅层、站台层、隧道、送风管、排风管、排烟风机、新风井、屏蔽门。顶部标题“地铁站通风系统”，副标题“看不见的空气怎样流动”。12个编号标注圈+短说明，四角信息面板：知识贴士/问题引导/小工程师/系统档案。底部流程“新风→送风→循环→排风→排烟”。现代写实+儿童科普绘本质感，深蓝+亮橙+白，中文清晰，无乱码，无水印。Style: educational-cutaway infographic
```

### 3. 垃圾分类流转系统

```text
竖版中文科普剖面海报，主题“垃圾分类流转系统”。画面是现代社区到城市处理厂的剖面流程：社区投放点、智能分类箱、厨余暂存、可回收压缩、垃圾转运站、分拣线、堆肥仓、焚烧发电、渗滤液处理。顶部标题“垃圾分类流转系统”，副标题“扔掉之后，它们去哪了”。12个编号标注圈+短说明，四角信息面板：知识贴士/问题引导/小督导员/城市档案。底部流程“投放→收运→分拣→处理→再利用”。现代写实+儿童科普绘本质感，深蓝+亮橙+白，中文清晰，无乱码，无水印。Style: educational-cutaway infographic
```

### 4. 城市供水净化系统

```text
竖版中文科普剖面海报，主题“城市供水净化系统”。画面从水库到居民厨房的剖面流程：取水口、沉砂池、絮凝池、沉淀池、过滤池、活性炭吸附、消毒间、清水池、加压泵站、城市管网、楼顶水箱、水龙头。顶部标题“城市供水净化系统”，副标题“一杯自来水的旅程”。12个编号标注圈+短说明，四角信息面板：知识贴士/问题引导/小水务员/城市档案。底部流程“取水→沉淀→过滤→消毒→入户”。现代写实+儿童科普绘本质感，深蓝+亮橙+白，中文清晰，无乱码，无水印。Style: educational-cutaway infographic
```

## Future topics

- 地铁防洪闸门系统
- 城市燃气安全系统
- 桥梁减震结构
- 高层建筑消防系统
- 数据中心冷却系统
- 机场行李分拣系统
- 变电站供电系统
- 城市污水处理系统

## Verification

After generation:
1. Save all images under `/Volumes/外接硬盘/hermes-images/daily-image-training/YYYY-MM-DD/` or a themed subdirectory.
2. Create `contact-sheet.jpg` for series review.
3. Run visual inspection on contact sheet: same style? correct themes? no obvious broken image/watermark/serious garbling?
4. Write a README with each prompt, file path, SHA256, and quality-check result.
5. Reply with `MEDIA:` links, including the contact sheet first.
