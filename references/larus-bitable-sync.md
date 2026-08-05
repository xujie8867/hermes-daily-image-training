# 拉鲁斯AI-提示词库 (Feishu Bitable) 同步指南

## 基本信息

- **飞书空间**: laruscanus
- **Base Token**: `SjrzbH91Rap24fsVVI2cap56npd`
- **Base 名称**: 拉鲁斯AI-提示词库

### 表结构

| 表名 | table_id | 字段 | 记录数 |
|------|----------|------|--------|
| 图片提示词库 | `tblvYM9KbArm705j` | 案例主题, 生图效果(attachment), 提示词 | 322 |
| 视频提示词库 | `tbl9YgYQbsJRAr5x` | 案例主题, 分镜图提示词, 分镜图效果(attachment) | 100 |

## 访问前提

1. **lark-cli 绑定到 Hermes**：`lark-cli config bind --identity user-default`
2. **用户授权**（首次或 token 过期时）：
   ```bash
   lark-cli config strict-mode off
   LARKSUITE_CLI_NO_UPDATE_NOTIFIER=1 lark-cli auth login --recommend --no-wait --json
   # 提取 verification_url → 生成二维码
   lark-cli auth qrcode "<verification_url>" --output "qr.png"
   # 用户扫码后完成
   lark-cli auth login --device-code "<device_code>"
   ```
3. **恢复 strict-mode**：操作完成后按需恢复 `lark-cli config strict-mode bot`

## 合并到本地提示词库

### JSON 格式关键陷阱
`lark-cli base +record-list --format json` 返回的 records 在 `data.data`（不是 `data.records`），且每条 record 是**数组** `[title, attachments_array, prompt_text]` 而非对象。

### 合并统计（2026-07-15）

| 来源 | 提取 | 新增 | 去重 |
|------|------|------|------|
| 图片提示词库 | 319 | 298 | 21 |
| 视频提示词库 | 77 | 77 | 0 |
| **总计** | **396** | **375** | **21** |

本地库：1,655 → 2,030

### 去重策略
比较 `prompt[:200]` 前缀，防止完全相同的提示词重复入库。

### 内容亮点
拉鲁斯库补全了社区库缺少的方向：电商详情页、写真人像POV、Logo品牌系统、餐饮商业、招商画册、像素游戏资产、立体书、体育海报、妆造提案。
