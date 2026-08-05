# Image-to-3D Providers 调研（2026-05-19）

> 基于 3DCellForge (huangserva/3DCellForge, 2188⭐) 源代码深度分析。
> 项目地址：https://github.com/huangserva/3DCellForge

## 全渠道对比

| Provider | 方式 | 费用 | 门槛 | 3DCellForge集成 |
|----------|------|:----:|:----:|:---------------:|
| **Hyper3D Rodin** | 云端 API | 💰 按量付费 | 低（只需 API Key） | ✅ 默认，`RODIN_API_KEY` |
| **Tripo** | 云端 API | 💰 按量付费 | 低（只需 API Key） | ✅ `TRIPO_API_KEY` |
| **Fal.ai** | 云端队列 | 💰 按量付费 | 低（只需 API Key） | ✅ `FAL_API_KEY`，内含5个模型 |
| **Hunyuan3D 本地** | 本地 GPU 部署 | **免费** | ❌ 需 NVIDIA GPU（≥8G显存） | ✅ `HUNYUAN_API_BASE=http://127.0.0.1:8081` |
| **JS Depth** | 浏览器端 | **免费** | 最低（纯前端，无需后端） | ✅ 兜底 |
| **Hunyuan3D via Fal.ai** | 云端 | 💰 按量付费 | 低 | ✅ `fal-ai/hunyuan3d/v2`（默认Fal模型） |

## 混元3D 两条路

### 方式一：本地部署（免费，需 GPU）
```env
HUNYUAN_API_BASE=http://127.0.0.1:8081
HUNYUAN_CREATE_PATH=/send
HUNYUAN_STATUS_PATH=/status
```
支持参数：`image_base64`、`prompt`、`remove_background`、`texture`、`pbr`、`octree_resolution`、`num_inference_steps`、`guidance_scale`、`face_count`。
生成结果可返回 `model_base64`/`glb_base64` 或远程URL。

### 方式二：通过 Fal.ai 云端（无需 GPU）
```env
FAL_API_KEY=your_fal_key
FAL_DEFAULT_MODEL=fal-ai/hunyuan3d/v2
```
Fal.ai 上可用5个图转3D模型：Hunyuan3D v2、TRELLIS、TripoSR、Tripo3D v2.5、Hyper3D Rodin。

## 3DCellForge 快速部署

```bash
git clone https://github.com/huangserva/3DCellForge.git
cd 3DCellForge
npm install
cp .env.example .env.local   # 填上至少一个 API Key
npm run dev:api &             # 后端 Node.js (端口8787)
npm run dev                   # 前端 Vite
```

## 架构要点

```
F/E (React + R3F + Three.js)
 ├── LeftSidebar — 模型库/生成队列
 ├── CenterStage — WebGL 3D舞台 (R3F + Drei)
 └── RightSidebar — 生成工具/设置
         │
         ▼ API
B/E (server.mjs, Node.js)
 ├── providers/rodin.mjs    ← Hyper3D (默认)
 ├── providers/tripo.mjs    ← Tripo
 ├── providers/fal.mjs      ← Fal.ai (含hunyuan3d v2)
 ├── providers/hunyuan.mjs  ← 本地混元3D
 └── providers/vision.mjs   ← GPT-4o-mini图片分析
```

### 亮点功能
- **智能运镜**：Demo Mode 根据模型类型自动切换——汽车低机位推进、飞机掠飞、船舰巡航、标本环绕
- **质量评分**：自动分析 GLB 文件大小、三角面数、贴图数量
- **视觉分析**：上传图片先用 GPT-4o-mini 识别物体类型，自动生成更好的 3D prompt
- **持久化**：IndexedDB 存模型记录、localStorage 兜底，刷新不丢
- **离线演示**：内置 demo GLB，不耗 API 也能展示
- **API Key 安全**：只存服务端 `.env.local`，不暴露到前端

## 使用场景

| 场景 | 推荐方案 |
|------|---------|
| 电商产品 360° 展示（传图出3D） | 3DCellForge + Fal.ai Hunyuan3D |
| 公众号嵌入可交互3D模型 | GLB文件可嵌入网页/小程序 |
| 零成本方案 | 本地部署混元3D（需 GPU 机器） |
| 快速验证 | Fal.ai 云端，仅需 API Key |
