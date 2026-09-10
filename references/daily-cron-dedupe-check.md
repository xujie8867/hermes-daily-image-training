# 每日 cron 输出验收 + 风格去重机制

> ⚠️ 2026-09-10 v6 精简：本文件的 dedup_check.py 180天 style_key 机制**已废弃**，当前每日生图去重以 SKILL.md「去重」一节为准（人物志30天 + 非人物题材30天 + 光影模板7天 + AM/PM互斥）。以下仅保留 cron 验收与故障恢复经验。

## Durable lesson

A cron run can report `last_status=ok` and create a file under today's date while still failing the user-facing requirement if it repeats yesterday's theme. Treat “new image file exists” as insufficient; the task is “new daily training output”.

## Verification checklist

1. Check actual current date/time.
2. Inspect today's output directory and README.
3. Inspect recent 7 days of output directories/READMEs.
4. Compare theme, city, visual formula, and file naming — not just file hash.
5. If today's output repeats yesterday's theme or merely reuses the same prompt pattern without a meaningful new subject, mark it incomplete and generate a fresh image immediately.
6. Save the new image with a theme-specific filename, e.g. `harbin-ice-life-map.png`, not only `image.png`.
7. Write a README note explaining why the new theme is not a duplicate.

## Response rule

If the user says the daily task did not run, do not argue from cron metadata alone. First validate the actual delivered artifact. If the user is right, acknowledge directly, fix it, then update the cron prompt/skill to prevent recurrence.

## Cron failure recovery (TimeoutError / idle timeout)

When the cron job reports `TimeoutError: Cron job ... idle for Ns (limit 600s) — last activity: executing tool: image_generate`:

### Diagnosis
1. Check `hermes cron list` for last run status
2. Verify `image_generate` still works: send a simple test prompt
3. Check OAuth: `hermes auth status openai-codex`

### Recovery workflow
1. **Test channel**: `image_generate` with a simple prompt (e.g., red apple on white table)
2. **If channel works** (most common — the timeout was transient): regenerate today's image immediately
3. **If OAuth expired**: `hermes auth add openai-codex` → re-authenticate → retest → regenerate
4. **If 外接硬盘 is not mounted**: use `~/.hermes/cache/images/` only as temporary cache, then backfill to `/Volumes/外接硬盘/hermes-images/daily-image-training/YYYY-MM-DD/`
5. **Write README** documenting the recovery

### 外接硬盘 fallback
When `/Volumes/外接硬盘` is not mounted (Permission denied), temporarily cache to:
```
~/.hermes/cache/images/
```
Do NOT treat the cache as final storage. Note it in the README and backfill to `/Volumes/外接硬盘/hermes-images/daily-image-training/YYYY-MM-DD/` after the disk is available.
