# 图生视频：图片公网 URL 托管方案

当 Agnes Video / Seedance / Veo 等视频 API 需要输入 `image` URL 参数时，本地图片必须先上传到公网可访问的直链。

## 已验证服务

| 服务 | 是否需要账号 | 有效期 | 直链格式 | 状态 |
|------|:---:|------|------|:---:|
| **litterbox.catbox.moe** | ❌ 无需 | 1h / 12h / 24h / 3d | `https://litter.catbox.moe/xxx.png` | ✅ 推荐 |
| tmpfiles.org | ❌ 无需 | 未知 | 不适用于 API | ❌ "Invalid image" |
| IMA COS URL | 需鉴权 | — | `res-pkb.ima.qq.com/...` | ❌ 需要 Cookie |
| gofile.io | ❌ 无需 | — | 下载页面非直链 | ❌ |

## litterbox.catbox.moe 使用方法

```bash
# 上传（1小时有效期）
curl -s -F "reqtype=fileupload" \
  -F "time=1h" \
  -F "fileToUpload=@/path/to/image.png" \
  "https://litterbox.catbox.moe/resources/internals/api.php"

# 返回直链：https://litter.catbox.moe/xxxxx.png
```

**有效期选项**：`1h` / `12h` / `24h` / `3d`

## 不可用的服务

- **0x0.st** — 因 AI botnet 滥用已禁用上传
- **catbox.moe**（非 litterbox）— 需要注册账号
- **file.io** — 301 重定向，不可用
- **imgbb.com** — 免费 API key 无效
- **postimages.org** — 不返回 JSON 直链

## 与 IMA 的关系

IMA 知识库的 `get_media_info` 返回的 URL（`res-pkb.ima.qq.com`）**不适用于第三方 API 调用**——需要 IMA Cookie 鉴权。如果需要同时入库 IMA 和传给视频 API，必须分两次上传：一次到 IMA（入库），一次到 litterbox（生成视频）。
