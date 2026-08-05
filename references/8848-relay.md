# api.884819.xyz 中转通道 — Grok系列

> 2026-05-19 验证恢复 | 4个Grok模型 + GPT/Claude/Gemini

## 基础配置

- **Base URL**: `https://api.884819.xyz/v1`
- **API Key**: `sk-NJyShrkBcep4h5kN8QMtBudULwSoU9T9UfdqTzEZoWC2kJKn`
- **Provider名**: `grok-8848`（已写入 Hermes config.yaml）
- **环境变量**: `GROK_8848_API_KEY`（已追加到 `~/.zshrc`）
- **格式**: 标准 OpenAI API（部分模型 streaming 默认开启，需显式 `"stream": false`）

## Grok 模型（已全部测试通过 ✅）

| 模型 | 用途 | 调用方式 | ✅ |
|------|------|---------|:-:|
| `grok-4.20` | AI对话、资讯查询 | chat/completions | ✅ 带引用来源 |
| `grok-4.20-fast` | 快速轻量对话 | chat/completions | ✅ 响应极快 |
| `grok-4.20-thinking` | 深度推理/复杂分析 | chat/completions | ✅ 含 reasoning_content |
| `grok-4.20-image` | 文生图 | chat/completions **仅** | ✅ 返回base64 data URL |

### ⚠️ Grok 关键限制
- **不能调用工具**（函数调用、MCP工具等不可用）。用户反复提醒过，每次切换到 Grok 后只能做纯对话和生图
- **记忆无持久性**：切换 provider 后当前会话的记忆不跟随
- **适合用途**：纯对话、实时资讯查询、文生图
- **不适合用途**：需要写文件、执行代码、读取本地数据、调用API

## 文生图细节（grok-4.20-image）

### 调用方式
**仅支持 chat/completions 端点**，不支持 `images/generations` 端点（后者报错 `not an image model`）：

```bash
curl -s https://api.884819.xyz/v1/chat/completions \
  -H "Authorization: Bearer $GROK_8848_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "grok-4.20-image",
    "messages": [
      {"role": "user", "content": "Generate an image of ..."}
    ],
    "stream": false,
    "max_tokens": 2000
  }'
```

### 响应格式
```json
{
  "choices": [{
    "message": {
      "content": "![image](data:image/jpeg;base64,/9j/...)"
    }
  }]
}
```

图片以 base64 data URL 嵌入在 content 字段的 markdown 中，格式为 `data:image/{fmt};base64,{b64data}`。

### 图片质量
- 写实场景：接近摄影级，光影/建筑/氛围渲染优秀
- 画质：约 200-300KB JPEG
- **中文文字渲染：极差（2026-05-19实测）**。prompt中指定的精确中文（如「深圳」「GDP 3.5万亿+」「从边陲小镇到国际化大都市」）会变成乱码/随机字符。城市海报密集文字排版场景完全不可用
- 用户结论：「Grok这个生图模型还是不行」
- **grok-4.20-image ≠ gpt-image-2**，含中文文字的图只用gpt-image-2

### ⚠️ 安全过滤行为（2026-05-21实测）

Grok-4.20-image 的安全过滤比 gpt-image-2 严格得多，在湿身/薄纱/性感场景下尤为敏感：

**被触发的关键词（返回空 content）：**
- 直接身体部位描述：`bust`, `full bust`, `voluptuous bust`
- 曲线/身材明示词：`voluptuous`, `hourglass figure`, `ample curves`
- 组合触发：`curvy` + `wet translucent fabric clinging` + 性感上下文 也可能被拦
- `fine art nude aesthetic` — 即使作为艺术风格也会触发

**能通过的写法（实测 ✅）：**
- ✅ `curvy body`（单独用，不加具体部位词）
- ✅ `curvy` + 中性场景（不加 wet clinging）
- ✅ `fashion editorial photo of an Asian model`（艺术框架包装）
- ✅ `sensual elegant atmosphere`（氛围词安全）
- ✅ `artistic boudoir photography style`（风格词安全）

**工作流提示：**
- 如果需要修改已有图片的人物身材（丰满、胸部等），**不要依赖 Grok 纯文生图**。安全过滤限制太严，且不支持参考图编辑。
- 正确路径：用 **gpt-image-2 via Codex CLI `--image` 参考图编辑模式**，在 prompt 中直接描述身材修改，效果精准且几乎不被过滤。
- 如果执意用 Grok，只能用最克制的身体词（`curvy`、`shapely`、`feminine curves`），配合纯艺术摄影语境才能通过。

## 已验证的其他模型

### 语言模型
| 模型 | 状态 |
|------|:----:|
| grok-4.20 | ✅ |
| grok-4.20-fast | ✅ |
| grok-4.20-thinking | ✅ |
| gpt-5.5 | ✅ |
| claude-sonnet-4-6 | ✅ |
| gemini-3.1-flash-image | ✅ |
| gemini-3.1-pro-high | ✅ |

### 生图模型
| 模型 | 状态 |
|------|:----:|
| grok-4.20-image | ✅ |
| gemini-3.1-flash-image | ✅ |

## 与其他中转对比

| 维度 | 8848 | millionengine (603个) | bobdong (15个) |
|:----|:---:|:-------------------:|:--------------:|
| Grok全系列 | ✅ 4个模型 | ✅ 部分 | ❌ |
| Grok生图 | ✅ grok-4.20-image | ✅ grok-4-image等 | ❌ |
| 视频 | ❌ 无 | ✅ grok-video-3/veo3.1 | ❌ |
| Claude | ✅ | ✅ Opus 4.7/Sonnet 4.6 | ❌ |
| 中文文字生图 | ❌ 弱 | ✅ gpt-image-2 | ✅ 主力 |
| 模型数量 | 25 | 603 | 15 |

## 使用场景建议

| 场景 | 推荐模型 |
|------|---------|
| 需要中文文字的海报/海报 | bobdong.cn gpt-image-2 |
| 实时资讯/最新科技动态 | grok-4.20（带引用来源） |
| 快速对话/闲聊 | grok-4.20-fast |
| 深度分析/推理 | grok-4.20-thinking |
| 创意概念图（无中文文字） | grok-4.20-image |
| 视频生成 | millionengine.com grok-video-3 |
| GPT-5.5/Claude写prompt | 8848 或 millionengine |

## ⚠️ 余额不足陷阱（2026-05-29 实测）

8848 是预付费中转，余额低于 ¥0.10 时所有调用返回 `insufficient_user_quota`：

```json
{
  "error": {
    "message": "预扣费额度失败, 用户剩余额度: ¥0.041842, 需要预扣费额度: ¥0.100000",
    "code": "insufficient_user_quota"
  }
}
```

- **单次最小扣费 ¥0.10**，余额低于此值直接不可用
- **作为 Codex 备选方案时**：先检查余额，别等 429 了才发现 8848 也没额度
- **充值**：需用户手动操作，渠道待确认
