# 参考图获取工作流（Search → Download → Generate）

> 当需要生成特定真实人物/产品/品牌的图片时，此流程是 mandatory 的。
> GPT-Image-2 的"世界知识"不等于精确还原，必须用真实照片作为参考图。

## 搜索渠道

### 首选：DuckDuckGo Images（无需翻墙）
```
Python方式：
1. 搜索 GET https://duckduckgo.com/?q={关键词}&iax=images&ia=images
2. 从HTML中提取 vqd token
3. GET https://duckduckgo.com/i.js?q={关键词}&vqd={vqd}&l=zh-cn&p=1
4. 从JSON results[].image 获取图片URL
5. 逐个下载
```

已验证可用的搜索关键词示例：
- `张雪 机车 创始人 照片` → 8张可用图片（最大423KB）
- `张雪机车 CX-4 摩托车` → 可用

### 备用：Bing Images
```
GET https://www.bing.com/images/search?q={关键词}
从HTML中提取 mediaurl 字段
```

## 下载与筛选

```python
# 按文件大小排序（越大通常质量越好）
files = sorted([(path, os.path.getsize(path)) for path in glob('*.jpg')], 
               key=lambda x: -x[1])
```

- 最大文件通常是人像/主视觉最佳候选
- 多张下载后用 vision_analyze 确认内容是否匹配需求

## Codex CLI 参考图生成模式

### 单参考图（最常见）
```bash
codex exec "生成一张[主题]海报。人像必须严格基于参考照片的脸部特征保留。
所有中文文字必须完整清晰无错别字。
[详细prompt]"
--image [portrait.jpg] --sandbox workspace-write
```

### 多参考图（需要控制角色+场景）
技巧6.9：GPT-Image-2 编辑模式支持最多16张参考图，角色分配：
```bash
codex exec "参考图角色：
Image 1: 人物肖像（人脸特征）
Image 2: 场景/产品参考

要求：基于Image 1保留人脸特征，参考Image 2的场景风格..."
--image [portrait.jpg] --image [scene.jpg] --sandbox workspace-write
```

## 已验证的搜索-生成案例

| 主题 | 搜索词 | 结果 |
|------|--------|------|
| 张雪机车海报 | `张雪 机车 创始人 照片` + `张雪机车 CX-4 摩托车` | 人物参考+摩托参考均有下载 |
| 手表变体 | 用户提供 | 直接用用户提供的图片 |
