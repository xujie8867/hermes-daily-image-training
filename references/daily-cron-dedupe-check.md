# 每日 cron 输出验收 + 风格去重机制

## 🔴 风格去重强制检查（Rule 0y）

**每次生图前必须执行，不管是 cron 还是手动。**

### 去重工具

位置：`/Volumes/外接硬盘/hermes-images/daily-image-training/dedup_check.py`

```bash
# 列出所有已用风格
python3 /Volumes/外接硬盘/hermes-images/daily-image-training/dedup_check.py

# 检查某个风格key是否可用
python3 /Volumes/外接硬盘/hermes-images/daily-image-training/dedup_check.py check <style_key>
# 退出码0=可用，退出码1=已存在（禁止使用）

# 标记风格为已使用
python3 /Volumes/外接硬盘/hermes-images/daily-image-training/dedup_check.py add <style_key> [YYYY-MM-DD]
```

### 风格key命名规则

```
{大类}-{子类}-{特征}
```

| 大类 | 示例key |
|------|---------|
| abstract | abstract-kintsugi, abstract-stained-glass, abstract-sem-macro, abstract-origami |
| portrait | portrait-hongkong-retro, portrait-french-lazy, portrait-sporty-tennis |
| infographic | infographic-city-cutaway, infographic-natural-field-guide |
| poster | poster-brand-kv, poster-city-artist-{artist} |
| ecommerce | ecommerce-luxury-watch, ecommerce-skincare-white |
| illustration | illustration-ghibli, illustration-ukiyoe, illustration-cyberpunk |

### 去重流程（每次生图必须过）

1. **选好风格后**：构造 style_key
2. **检查历史**：`python3 dedup_check.py check <style_key>`
3. **被阻塞** → 换大类，不要在同大类内换子类
4. **生成完** → `python3 dedup_check.py add <style_key>` 立即标记
5. **180天内不重复**：同一 style_key 180天内不再生成

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
