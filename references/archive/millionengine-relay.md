# millionengine.com 中转通道

> 已验证 2026-05-17 | 603个模型 | 生图+生视频+语言全支持

## 基础配置

- **Base URL**: `https://millionengine.com/v1`
- **API Key**: `sk-hyO5acRtIMTsf2n2TgbZkDNc9KtFi75P0hXBuyUdLup4NuP6`
- **格式**: 标准 OpenAI API（部分模型兼容）

## 已验证可用的核心模型

### 🎬 生视频（核心价值！）

| 模型 | 调用方式 | 说明 |
|------|---------|------|
| `grok-video-3` | chat/completions | 最稳，返回进度+MP4链接 |
| `grok-video-3-10s` | chat/completions | 10秒版本 |

**调用示例**：
```python
payload = {
    "model": "grok-video-3",
    "messages": [{"role": "user", "content": [{"type": "text", "text": "描述视频内容"}]}]
}
# POST /v1/chat/completions
# 返回 choices[0].message.content 包含进度和下载链接
```

**响应格式**：
```
> 当前进度: 1%
> 当前进度: 5%
...
> 当前进度: 95%

视频生成成功
![image](https://...thumbnail.jpg)
[点击下载视频](https://...video.mp4)
```

### 🖼️ 生图（待全面测试）

| 模型 | 端点 |
|------|------|
| `gpt-image-2` / `gpt-image-2-all` | chat/completions |
| `gpt-image-1.5` / `gpt-image-1` | chat/completions |
| `flux-2-pro` / `flux-1.1-pro` | chat/completions |
| `grok-imagine-image` / `grok-imagine-image-pro` | chat/completions |
| `grok-4-image` / `grok-4.1-image` / `grok-4.2-image` | chat/completions |
| `dall-e-3` | images/generations |
| `qwen-image-2.0` / `qwen-image-2.0-pro` | chat/completions |
| `z-image-turbo` | chat/completions |
| `mj_imagine` / `mj_blend` / `mj_upscale` 等全套 | Midjourney 兼容 |

### 🤖 语言模型

| 类别 | 模型 | 状态 |
|------|------|:----:|
| GPT-5 | `gpt-5.5`, `gpt-5.4`, `gpt-5.4-pro`, `gpt-5.3-codex` | ✅ |
| Claude | `claude-opus-4-7`, `claude-sonnet-4-6`, `claude-haiku-4-5` | ✅ |
| Grok | `grok-4.3`, `grok-4.2`, `grok-4.1`, `grok-4`, `grok-4-fast` | ✅ |
| DeepSeek | `deepseek-v4-pro`, `deepseek-v4-flash`, `deepseek-v3.2`, `deepseek-r1` | ✅ |
| Qwen | `qwen3.6-plus`, `qwen3.5-plus`, `qwen3.5-flash` | ✅ |
| Kimi | `kimi-k2.6`, `kimi-k2.5`, `kimi-k2` | ✅ |
| o系列 | `o4-mini`, `o3-pro`, `o3-mini`, `o1` | ✅ |
| GLM | `glm-4.7`, `glm-4.6`, `glm-4.5` | ✅ |

### 🎬 其他视频模型（待测）

- `veo2` / `veo2-pro` / `veo2-fast`
- `veo3.1` / `veo3.1-pro` / `veo3.1-4k`
- `kling-video` / `kling-omni-video`
- `wan2.6-i2v` / `wan2.5-i2v-preview`
- `happyhorse-1.0-t2v` / `happyhorse-1.0-i2v`
- `viduq3` / `viduq3-pro`
- `mimo-v2.5-pro`
- `mj_video`

## 与其他中转对比

| 维度 | millionengine (603个) | bobdong (15个) | 8848 (25个) |
|:----|:-------------------:|:--------------:|:----------:|
| 视频 | ✅ grok-video-3/veo3.1/kling | ❌ seedance断流 | ❌ 无 |
| Claude | ✅ Opus 4.7/Sonnet 4.6 | ❌ | ✅ |
| Flux/MJ | ✅ flux-2-pro/MJ全套 | ❌ | ❌ |
| 中文文字 | ✅ gpt-image-2可用 | ✅ 主力 | ❌ 无生图 |
| 模型数量 | 603 | 15 | 25 |

## 注意事项

- 视频生成约 2-3 分钟，chat/completions 返回含进度信息
- 部分模型可能需通过 chat/completions 而非 images/generations 端点
- API key 额度未知，使用注意监控
- 生图待全面测试验证
