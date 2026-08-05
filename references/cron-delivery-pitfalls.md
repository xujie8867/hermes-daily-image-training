# Cron 生图任务交付失败处理

## 问题（2026-07-02 实测）

每日 cron 生图任务（daily-image-training）`last_status: ok`，但生成的图片未发送到飞书对话。

### 症状
- `cronjob action=list` 显示 `last_status: ok`, `last_delivery_error: null`
- `~/.hermes/cache/images/` 有当天 4 张图（时间戳在 cron 执行时间前后）
- 但用户没收到任何 MEDIA: 消息

### 根因猜测
- `deliver: origin` 在 Feishu 网关通道可能未正确路由回当前对话
- cron 子进程的 Feishu adapter 可能未初始化或会话上下文丢失

## 恢复流程

1. **验证 cron 确实生成了图**：
   ```bash
   ls -la ~/.hermes/cache/images/openai_codex_gpt-image-2-medium_YYYYMMDD_*.png
   ```

2. **vision_analyze 确认 4 张主题**（用于查重和避免重复主题）

3. **直接手动发送 MEDIA: 路径** 给用户

4. **如果用户要求比例修正**：按正确比例重新生成（不要只是裁剪旧图）

5. **不要依赖 `last_status: ok` 作为「用户看到了」的信号** — cron 成功 ≠ 交付成功

## 预防

- 每日 cron 执行后的下一手动会话，主动检查是否收到了 cron 输出
- 如果用户说「今天生图了吗」/「生图完成了吗」= cron 交付失败，走上述恢复流程
