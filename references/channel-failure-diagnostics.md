# 生图通道全部失败时的诊断流程

> 当 image_generate 返回 timeout / 403 / 空响应时，不要反复重试同一通道。
> 走下面这个流程，每次只多花 2-3 轮，快速定位是哪个环节卡住了。

## 诊断顺序（按优先级）

### 1. 最小 prompt 测试主力通道

```
image_generate(prompt="A cup of tea on a table", aspect_ratio="portrait")
```

如果连 5 个单词的 prompt 都超时，说明不是 prompt 问题，是通道本身坏了。
**不要**反复换 prompt 重试 — 这是最常见的误区。

### 2. 查环境变量

```python
# execute_code 中跑
import subprocess
r = subprocess.run(['bash', '-c', 'source ~/.zshrc 2>/dev/null && env | grep -E "GROK_8848|AGNES_API|DFA_API|BOBDONG|MILLIONENGINE"'], 
    capture_output=True, text=True)
print(r.stdout)
```

注意：`~/.zshrc` 中的变量不会自动出现在 Hermes 的终端/execute_code 环境中，
每次需要 source 后再拿。

### 3. 逐通道验证

| 通道 | 快速验证方法 |
|------|------------|
| openai-codex | `image_generate` 最小 prompt → timeout 则 OAuth 过期 |
| Grok 8848 | `GET /v1/models` → 403 code 1010 = key 失效 |
| Agnes | `POST /v1/images/generations` → 404 HTML 页面 = key 失效 |
| Codex MCP | `mcp_codex_desktop_codex` → 300s timeout = 同 openai-codex OAuth |

### 4. 常见失效模式速查

| 症状 | 根因 | 修复 |
|------|------|------|
| `image_generate` timeout（即使最短prompt） | openai-codex OAuth 过期 | 用户需在 Codex.app 重新登入 OpenAI 账号 |
| Grok 8848 HTTP 403 `error code: 1010` | API key 被禁用/余额不足 | 用户需重新获取 8848 API key |
| Agnes HTTP 404 返回 HTML 页面 | API key 无效/格式错误 | 用户需在 console.agnes-ai.com 重新生成 |
| Codex MCP 300s timeout | 同 openai-codex OAuth | 同上 |

### 5. 汇报格式

诊断完直接给用户一张表，不要长篇解释。格式：

```
| 通道 | 状态 | 原因 |
|------|------|------|
| image_generate | ❌ 3次超时 | OAuth 过期 |
| Grok 8848 | ❌ 403 | Key 失效 |
| Agnes | ❌ Key缺失 | 环境变量为空 |
```

## 陷阱

- **不要**在同一次会话中重复调用失败的 `image_generate` 超过 3 次 — 工具会触发 `same_tool_failure_warning`
- **不要**在 shell 中拼接 API key 到 curl 命令 — 终端会打码/转义导致语法错误。用 execute_code + Python `urllib.request` 替代
- **不要**等所有通道确认后再汇报 — 测出一个失败就记录，并行测其他
