# Food lifecycle ring infographic

Use this reference when the user asks for a food-science infographic like “{食物名称}的一生”, especially after correcting away from slice/cutaway layouts.

## Correct visual formula

The user-approved correction is **not** a single food horizontally cut into maturity slices. The desired form is:

- One complete circular lifecycle composition.
- 4-6 complete single food items placed evenly around the ring.
- Each stage is a full intact unit (e.g. one complete banana per stage), not a fragment, cross-section, or chopped slice.
- Arrows connect stages around the circle.
- The ring should read as a lifecycle / time loop infographic.
- Each stage gets a nearby Chinese info card.

## Stage card content

For each stage include:

1. 阶段名称
2. 外观特点
3. 内部变化（糖分 / 淀粉 / 水分 / 组织变化）
4. 食用建议（推荐 / 适合烹饪 / 尽快食用 / 不建议 / 不可食用）
5. ✔️ / ⚠️ icons where useful

## Prompt skeleton

```text
竖版3:4中文科普信息图，标题“{食物名称}的一生”。米色极简小红书风，高真实感摄影。画面中心是一个完整圆环时间轴，沿圆环均匀摆放{N}个完整{食物名称}，每个阶段都是完整单体：{阶段1}→{阶段2}→{阶段3}→{阶段4}[→{阶段5}]，首尾用箭头连接成生命周期环。每阶段旁写：阶段名、外观、内部变化、食用建议，配✔️⚠️。要求圆环构图清晰，不要横向切片，不要碎块，不要截面拼接。中文清晰，无水印。
```

## Example: banana

```text
竖版3:4中文科普信息图，标题“香蕉的一生”。米色极简小红书风，高真实感摄影。画面中心是一个完整圆环时间轴，沿圆环均匀摆放5根完整香蕉，每根都是完整单体：青绿未熟→金黄成熟→黑斑过熟→软皱出水→发霉腐坏，首尾用箭头连接成生命周期环。每阶段旁写：阶段名、外观、内部变化、食用建议，配✔️⚠️。要求圆环构图清晰，不要横向切片，不要香蕉碎块。中文清晰，无水印。
```

## Pitfall

If the initial user prompt says “横向切片 / 同一个食物随时间变化的切片” but then corrects to “每个阶段一个完整的香蕉，整个图呈现一个完整的圆环”, obey the correction. The correction supersedes the earlier slice wording.
