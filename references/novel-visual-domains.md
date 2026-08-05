# 全新视觉域（视觉疲劳时的跨域跳转目标）

> 当用户说「视觉疲劳」「这类风格看腻了」，且冷门提示词挖掘后仍然不满足时，跳转到这些域。
> 核心理念：不挖更稀有的提示词，而是换一个完全不同的「看世界的方式」。

## 材质/光实验域（优先级1）

这些不是「画什么」，而是「用什么材质、什么光来看」。Prompt 构建模板见 `abstract-material-art` 技能。

| 风格 | Prompt 关键词 | 视觉效果 | 用户反馈 |
|------|-------------|---------|---------|
| **金缮 (Kintsugi)** | shattered celadon ceramic + gold lacquer veins, macro close-up, dark background, dramatic side lighting | 破碎青瓷的金色裂纹，修复美学 | ✅ 满意 |
| **彩色玻璃 (Stained Glass)** | cathedral rose window, jewel-toned glass, lead came lines, backlight streaming through | 光穿透宝石色玻璃，哥特建筑 | ✅ 满意 |
| **电子显微镜 (SEM False-Color)** | SEM of butterfly wing scales, extreme magnification, false-color cyan/indigo, shallow DOF | 微观结构的异星建筑感 | ✅ 满意 |
| **折纸光影 (Origami Chiaroscuro)** | washi paper geometric folds, single spotlight, extreme chiaroscuro, ivory/cream palette | 纯几何+影，没有内容，只有空间和光 | ✅ 满意 |
| **X光艺术** | X-ray radiography, translucent overlapping forms, ethereal blue-white glow | 穿透表象看内部结构 | 待测试 |
| **烙画 (Pyrography)** | wood burning art, scorched grain patterns, warm sepia tones | 火烧木纹的有机纹理 | 待测试 |
| **沙画 (Sand Art)** | colored sand layered on lightbox, translucent granular texture, backlit | 颗粒层的半透明叠加 | 待测试 |
| **冰雕/雪雕** | ice sculpture, frozen crystal facets, cold blue light refraction | 冻结的光学折射 | 待测试 |

## 真人摄影域（优先级2）

使用 `female-portrait-director` 技能，14 种摄影风格可选。关键：这些是「拍出来的」不是「画出来的」。

| 风格 | Route ID | 一句话 | 用户反馈 |
|------|----------|--------|---------|
| 复古港风 | retro-hongkong | 90s 香港电影剧照，霓虹+胶片，王家卫美学 | ✅ 满意 |
| 法式慵懒 | french-lazy | 巴黎阳台晨光，Jeanne Damas effortless chic | ✅ 满意 |
| 活力运动 | sporty-active | 运动场动态抓拍，网球发球瞬间，汗水+阳光 | ✅ 满意 |
| 旅行假日 | travel-vacation | 圣托里尼黄金时刻，海风草帽，度假随拍 | ✅ 满意 |
| 都市时尚 | urban-fashion | 城市街拍OOTD | 待测试 |
| 清纯生活 | clean-lifestyle | 咖啡馆窗边，温柔自然光 | 待测试 |

完整 14 条风格见 `references/female-portrait-styles.md`。

## 科学视觉域（优先级3）

用科学仪器视角代替人类/艺术家视角。

| 风格 | Prompt 关键词 | 视觉效果 |
|------|-------------|---------|
| **岩石薄片 (Petrography)** | mineral thin section, crossed polarizers, interference colors, geometric crystal patterns | 偏光显微镜下的矿物万花筒 |
| **色谱艺术** | paper chromatography, separated pigment bands, scientific lab aesthetic | 滤纸上的色彩分离 |
| **菌落艺术** | bacterial colony on agar plate, bioluminescent patterns, petri dish photography | 培养皿中的微生物图案 |
| **热成像** | thermal infrared photography, false-color heat map, urban heat island | 温度的可视化 |
| **声波/振动** | cymatics, sound wave patterns on water/sand, Chladni figures | 声音的物理形态 |

## 使用原则

1. **用户说「视觉疲劳」→ 先试第一级（冷门提示词挖掘）**
2. **第一级后仍不满足 → 跳转到本表的优先级 1（材质/光实验）**
3. **用户发回满意图 → 确认该域有效，标记 ✅**
4. **每个域内选 4 个不同风格，不要重复同一域的同一种**

## 已验证成功的组合

| 日期 | 域 | 4 张 | 用户反馈 |
|------|-----|------|---------|
| 2026-07-15 | 材质/光实验 | 金缮 + 彩玻 + SEM显微 + 折纸光影 | ✅ 全部满意 |
| 2026-07-15 | 真人摄影 | 复古港风 + 法式慵懒 + 活力运动 + 旅行假日 | ✅ 全部满意 |

## 提示词库扩展工作流

当用户分享新 prompt 源（GitHub 仓库、飞书多维表格），加载 `prompt-library-curation` 技能：
1. 搜索/解析源 → 2. 提取 prompt → 3. 去重合并到 `all-prompts.json`
2. 当前库规模：2,392 条（来自 8 个来源）
3. 来源清单：freestylefly + image-inspirer + DavidWu + peterRooo + 拉鲁斯AI图片 + 拉鲁斯AI视频 + Awesome-AI-Image-Prompts + awesome-gpt4o-images
