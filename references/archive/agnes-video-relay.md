# Agnes Video V2.0 中转通道

## 基本信息

| 项目 | 内容 |
|------|------|
| 提供商 | Sapiens AI（新加坡） |
| 模型名 | `agnes-video-v2.0` |
| API 网关 | `https://apihub.agnes-ai.com` |
| 认证 | Bearer Token |
| 价格 | **$0/秒（当前免费，2026-06-09）** |
| 方式 | 异步：创建任务 → 轮询结果 |
| 文档 | https://agnes-ai.com/doc/agnes-video-v20 |

## 注册获取 API Key

1. 打开 https://console.agnes-ai.com/register
2. 支持 **GitHub 登录**（推荐）或邮箱注册
3. 登录后进入 API Key 管理页面，创建并复制 Key
4. 控制台地址：https://console.agnes-ai.com

> ⚠️ 控制台与主站不在同一域名（console.agnes-ai.com vs agnes-ai.com），且是 SPA 应用，直接 curl 无法获取页面内容。

## 四种生成模式

| 模式 | 输入 | 参数 | 用途 |
|------|------|------|------|
| 文生视频 | `prompt` | 仅需 prompt + model | 从零生成 |
| 图生视频 | `prompt` + `image`(单URL) | image 字段 | 图片动画化 |
| 多图视频 | `prompt` + `extra_body.image`(数组) | extra_body | 多图间过渡 |
| 关键帧动画 | `prompt` + `extra_body.image`(数组) + `extra_body.mode:"keyframes"` | extra_body | 关键帧平滑过渡 |

## API 调用

### 创建任务

```bash
POST https://apihub.agnes-ai.com/v1/videos
Authorization: Bearer <API_KEY>
Content-Type: application/json

{
  "model": "agnes-video-v2.0",
  "prompt": "A cat walking on the beach at sunset...",
  "height": 768,
  "width": 1152,
  "num_frames": 121,
  "frame_rate": 24
}
```

响应：返回 `task_id` 和 `video_id`，推荐用 `video_id` 查询。

### 查询结果（推荐方式）

```bash
GET https://apihub.agnes-ai.com/agnesapi?video_id=<VIDEO_ID>
Authorization: Bearer <API_KEY>
```

建议轮询间隔 5 秒。`status: "completed"` 时，`remixed_from_video_id` 字段为视频 URL。

### 查询结果（兼容旧方式）

```bash
GET https://apihub.agnes-ai.com/v1/videos/<TASK_ID>
Authorization: Bearer <API_KEY>
```

## 视频参数

| 参数 | 默认值 | 限制 | 说明 |
|------|--------|------|------|
| `width` × `height` | 1152×768 | — | 视频分辨率 |
| `num_frames` | — | ≤441, 必须 `8n+1` | 帧数：81/121/161/241/441 |
| `frame_rate` | — | 1-60 | FPS |
| `seed` | — | — | 固定种子可复现 |
| `negative_prompt` | — | — | 负向提示词 |

**时长公式**：`seconds = num_frames / frame_rate`

| 目标时长 | 推荐参数 |
|----------|---------|
| ~3 秒 | `num_frames: 81, frame_rate: 24` |
| ~5 秒 | `num_frames: 121, frame_rate: 24` |
| ~10 秒 | `num_frames: 241, frame_rate: 24` |
| ~18 秒 | `num_frames: 441, frame_rate: 24` |

## 任务状态

| 状态 | 说明 |
|------|------|
| `queued` | 排队等待 |
| `in_progress` | 生成中 |
| `completed` | 完成，`remixed_from_video_id` 可用 |
| `failed` | 失败 |

## Prompt 最佳实践

### 文生视频公式
```
[主体] + [动作] + [场景] + [镜头运动] + [光照] + [风格]
```

### 图生视频
描述需要运动的内容 + 保持稳定的元素：
```
Animate the character with subtle breathing, hair moving in wind, 
while keeping face and outfit consistent
```

### 关键帧动画
描述关键帧之间的过渡关系：
```
Smooth transition from first keyframe to second, maintaining 
character identity, consistent camera angle, natural motion
```

## 在 Hermes 中的定位

- 作为 `image_generate` 的视频补充：gpt-image-2 生图 → 上传获 URL → Agnes Video 图生视频
- 与现有 millionengine (Veo 3.1/grok-video-3)、bobdong (Seedance) 并列，优先用于 **免费** 场景
- 中文文字渲染未测试，宣传图/海报类建议先出图再用图生视频模式

## ⚠️ 实战踩坑（2026-06-09）

### 图生视频：图片 URL 必须公开可访问

Agnes API 的 `image` 参数需要**公网直链**。以下 URL 类型不可用：

| URL 类型 | 示例 | 结果 |
|----------|------|------|
| IMA 知识库 URL | `res-pkb.ima.qq.com/...` | ❌ 401 "无效的令牌" — 需要 Cookie 鉴权 |
| tmpfiles.org | `tmpfiles.org/dl/...` | ❌ "Invalid image" — 尽管 HTTP 200，API 无法读取 |
| gofile.io | `gofile.io/d/...` | ❌ 返回下载页面而非直链 |
| ✅ litterbox.catbox.moe | `litter.catbox.moe/xxx.png` | ✅ 直链可工作 |

**推荐图床**：`litterbox.catbox.moe` — 临时上传（1小时有效）、无需账号、返回直链。
详见 `references/image-url-hosting.md`。

### API Key 注意事项

- Key 含特殊字符时，不要直接嵌入 Python/Shell 源码——会被 Hermes 的安全过滤系统改写为 `***` 导致语法错误
- 正确做法：将 Key 写入临时文件 → Python `open().read().strip()` 读取 → 用于 API 调用
- Hermes 配置存储：`hermes config set providers.agnes-video.api_key` 自动写入 `~/.hermes/config.yaml`
- 首次测试发现文生视频可用，但之后返回 401——Key 可能有时效性，需用户重新生成

### 轮询策略

- 创建任务后约 50-60 秒完成（121帧@24fps≈5秒视频）
- 进度从 `10%` 跳到 `80%` 再跳到 `100%`，不是线性增长
- 轮询间隔 5 秒，最长等待 15 轮（75 秒）
