#!/usr/bin/env python3
"""
prepare_daily_batch.py - 每日生图前置批处理准备脚本 (v1.0.0)
功能：
1. 3秒内完成过去30天历史生成去重（建筑、风景、人像题材）。
2. 根据当天是周几自动分流：
   - 周一至周五：01-03 从词库采样3条独立顶级人像Prompt（不限林晚、不限风格）；
   - 周六周日：01固定林晚拉鲁斯海报，02/03做1:1水彩与线稿复刻配置；
   - 04-05：建筑、风景（严格排除30天历史）；
   - 06-07：两座不同城市的国风文旅叙事长卷海报（城市30天去重）。
3. 自动在 work/ 目录下生成结构化配置，避免 Agent 盲目空转试错。
"""

import os
import sys
import json
import random
import datetime
import argparse

BASE_DIR = os.path.expanduser("~/hermes-daily-image-training")
DATA_PROMPTS_PATH = os.path.join(BASE_DIR, "data", "all-prompts.json")
VOLUMES_BASE = "/Volumes/外接硬盘/hermes-images/daily-image-training"

# 知名建筑池（严格去重）
ARCHITECTURE_POOL = [
    ("Rome Pantheon", "Interior view of the Pantheon in Rome, monumental ancient Roman concrete dome with central oculus, solitary light beam cutting through ancient dust, floor polished marble geometric patterns, silent sacred atmosphere, architectural photography, shot on Hasselblad H6D-100c, tilt-shift lens 24mm, f/8, natural dramatic lighting, ultra-fine details, 8k, no people, empty scene"),
    ("Taj Mahal Dawn", "Dawn view of the Taj Mahal in Agra, pristine white ivory marble reflecting faint soft rose and pale gold morning mist over the tranquil Yamuna river, symmetrical Mughal architecture, intricate floral marble inlays, serene mist, no people, empty scene, shot on Fujifilm GFX 100S, 45mm lens, f/11, ethereal morning light"),
    ("Milan Duomo Roof", "High-angle perspective on the marble spires and pinnacles of the Milan Cathedral Duomo, intricate Italian Gothic stone lacework against deep sapphire twilight sky, dramatic architectural shadows, razor-sharp carved marble details, shot on Phase One IQ4, 35mm, f/8, no people, empty scene"),
    ("Sagrada Familia Nave", "Interior forest of soaring tree-like stone columns inside the Sagrada Familia in Barcelona, kaleidoscope of vivid geometric stained glass reflections on pale ribbed vaults, organic Catalan Modernisme architecture, atmospheric dust motes, tilt-shift 17mm, f/8, golden afternoon sun, no people, empty scene"),
    ("Parthenon Sunset", "The Parthenon temple on the Acropolis of Athens, monumental weathered Pentelic marble Doric columns bathed in deep amber sunset glow, ancient cracked stone steps, dramatic classical Mediterranean sky, architectural masterwork, Hasselblad 50mm, f/9, no people, empty scene"),
    ("St. Basil Cathedral Snow", "St. Basil Cathedral in Moscow covered in crisp fresh winter snowfall, vivid multicolored patterned onion domes contrasting with deep blue winter dusk, intricate Russian revival brickwork, clean snow untouched, cinematic architectural lighting, no people, empty scene"),
    ("Mont Saint-Michel High Tide", "Mont Saint-Michel medieval tidal island commune rising out of shimmering tidal waters at dusk, dramatic granite abbey spire silhouetted against twilight purple clouds, ancient stone ramparts, long exposure reflections, Hasselblad 35mm, no people, empty scene"),
    ("Alhambra Court of the Lions", "Court of the Lions inside the Alhambra in Granada, 124 slender white marble columns supporting exquisite Moorish stalactite stucco arches and arabesques, central carved marble fountain basin, warm Mediterranean morning shadow, no people, empty scene")
]

# 意境风景池（严格去重）
LANDSCAPE_POOL = [
    ("Moraine Lake Dawn", "Moraine Lake in Banff National Park at early dawn, glassy turquoise glacial water perfectly mirroring the rugged Ten Peaks dusted in fresh snow, golden alpine larches framing the rocky shoreline, crisp mountain air, 8k nature photography, Hasselblad 28mm, f/11, no people, empty scene"),
    ("Namib Sossusvlei Dunes", "Towering terracotta and burnt-orange sand dunes of Sossusvlei in the Namib Desert, razor-sharp ridge lines dividing deep violet shadows and brilliant morning sunlight, dead camel thorn trees in cracked white clay pan, abstract geological minimalism, Phase One 80mm, f/11, no people, empty scene"),
    ("Iceland Diamond Beach", "Diamond Beach in Iceland, glistening crystalline glacial ice blocks scattered across deep black basalt sand, crashing turquoise Arctic surf in long exposure, dramatic midnight sun glow on ice facets, macro-wide perspective, no people, empty scene"),
    ("Lofoten Winter Fjords", "Snowcapped jagged granite peaks rising directly from deep sapphire Arctic waters in Lofoten Islands, soft pastel arctic twilight, pristine untouched snow, ethereal calm fjord reflection, Leica S3, 30mm, no people, empty scene"),
    ("Zhangjiajie Misty Pinnacles", "Towering quartzite sandstone pillars of Zhangjiajie rising through swirling sea of white valley fog, gnarled ancient pine trees clinging to sheer vertical cliffs, traditional Chinese ink painting atmosphere realized in photorealistic 8k, Hasselblad 45mm, no people, empty scene"),
    ("Tuscan Rolling Hills", "Rolling emerald and golden wheat hills of Val d'Orcia in Tuscany at sunrise, solitary winding dirt road lined with slender Italian cypress trees, gentle valley ground mist, warm golden hour backlighting, medium format landscape, no people, empty scene")
]

# 国风城市文旅海报池。每项只使用可核验的城市地标、建筑、非遗和风物，禁止跨城混搭。
CITY_POSTER_POOL = [
    {
        "slug": "dongguan-lingnan-scroll",
        "city": "东莞",
        "english": "DONGGUAN · CHINA",
        "title": "莞邑流芳",
        "seal": "岭南莞邑",
        "palette": "lychee red, banyan green, warm ivory and seal vermilion",
        "evidence": "Humen Weiyuan Fort, Keyuan Garden, arcaded Lingnan streets, dragon boat craftsmanship, lychees and blooming kapok",
        "figure": "a local craftsperson working on a dragon boat ornament"
    },
    {
        "slug": "quanzhou-maritime-scroll",
        "city": "泉州",
        "english": "QUANZHOU · CHINA",
        "title": "刺桐海丝",
        "seal": "海丝泉州",
        "palette": "brick red, ocean teal, warm ivory and seal vermilion",
        "evidence": "Kaiyuan Temple twin pagodas, Luoyang Bridge, red-brick swallowtail-roof houses, maritime sailing vessels, Dehua porcelain and puppet carving",
        "figure": "a quiet artisan painting a Dehua porcelain piece"
    },
    {
        "slug": "suzhou-garden-scroll",
        "city": "苏州",
        "english": "SUZHOU · CHINA",
        "title": "姑苏雅韵",
        "seal": "水巷姑苏",
        "palette": "ink green, celadon blue, warm ivory and seal vermilion",
        "evidence": "Humble Administrator's Garden, Tiger Hill Pagoda, white-walled black-tiled canal houses, stone bridges, Suzhou embroidery and silk",
        "figure": "an embroiderer working beside a garden lattice window"
    },
    {
        "slug": "xian-changan-scroll",
        "city": "西安",
        "english": "XI'AN · CHINA",
        "title": "长安古意",
        "seal": "千年长安",
        "palette": "mineral blue, earthen ochre, warm ivory and seal vermilion",
        "evidence": "Xi'an City Wall, Giant Wild Goose Pagoda, Tang-style eaves, bronze lamps, pomegranates and traditional shadow-puppet craft",
        "figure": "a shadow-puppet artisan carving translucent leather"
    },
    {
        "slug": "hangzhou-westlake-scroll",
        "city": "杭州",
        "english": "HANGZHOU · CHINA",
        "title": "湖山清韵",
        "seal": "西湖杭州",
        "palette": "lotus green, mist blue, warm ivory and seal vermilion",
        "evidence": "West Lake, Leifeng Pagoda, Broken Bridge, Jiangnan garden pavilions, Longjing tea terraces, silk umbrellas and lotus",
        "figure": "a tea maker preparing Longjing leaves beside a bamboo tray"
    },
    {
        "slug": "dunhuang-silkroad-scroll",
        "city": "敦煌",
        "english": "DUNHUANG · CHINA",
        "title": "大漠敦煌",
        "seal": "丝路敦煌",
        "palette": "mineral turquoise, desert gold, warm ivory and seal vermilion",
        "evidence": "Mogao Grotto cliff facade, Crescent Lake and Mingsha dunes, Silk Road camel route, apsara-inspired ribbon motifs and Dunhuang mural pigments",
        "figure": "a mural conservator carefully preparing mineral pigments"
    }
]

def build_city_poster_prompt(item):
    """生成无字底图；准确文字交由本地排版，避免模型乱码。"""
    return (
        "Premium Chinese cultural-tourism editorial poster, vertical 2:3 portrait. "
        "Use an asymmetrical magazine composition: reserve the left 30 percent as clean warm-ivory handmade Xuan-paper negative space for later typography; "
        "the right 70 percent forms one continuous S-shaped narrative scroll, never a rectangular photo collage. "
        f"This poster is exclusively about {item['city']}, China. Use only these verified local elements: {item['evidence']}. "
        "Right upper area: recognizable natural setting and landmark architecture; middle area: traditional architecture and local craft; "
        f"right lower area: {item['figure']}, shown at three-quarter view facing inward, with accurate hands and believable working action. "
        "Connect all layers with locally appropriate plants, water, cloud mist, silk ribbons and restrained ink-wash curves so every element appears to grow naturally from the scroll. "
        "Blend precise documentary architectural detail with translucent Eastern watercolor, dry-brush Xuan-paper edges, subtle print grain and generous breathing space. "
        f"Color palette: {item['palette']}. Clear foreground, middle ground and distance; refined museum-catalogue quality, not a cheap tourism flyer. "
        "STRICTLY NO text, letters, calligraphy, seals, logo or watermark in the generated base image; keep the left column empty and unobstructed for deterministic local typography. "
        "No mixed-city landmarks, no mismatched ethnic clothing, no giant face silhouette, no double exposure, no nine-grid collage, no hard rectangular frames, no neon colors, no plastic 3D render."
    )

def load_history_used_terms(days=30):
    used_titles = set()
    used_architectures = set()
    used_landscapes = set()
    
    if not os.path.exists(VOLUMES_BASE):
        return used_titles, used_architectures, used_landscapes
        
    cutoff_date = (datetime.datetime.now() - datetime.timedelta(days=days)).strftime("%Y-%m-%d")
    
    try:
        entries = sorted(os.listdir(VOLUMES_BASE))
    except Exception:
        return used_titles, used_architectures, used_landscapes

    for folder in entries:
        if not folder.startswith("2026-") or folder < cutoff_date:
            continue
        meta_file = os.path.join(VOLUMES_BASE, folder, "meta.json")
        if not os.path.isfile(meta_file):
            continue
        try:
            with open(meta_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            # data could be list or dict
            images = []
            if isinstance(data, dict):
                images = data.get("images", [])
            elif isinstance(data, list):
                images = data
            for item in images:
                if isinstance(item, dict):
                    title = item.get("title", "")
                    prompt = item.get("prompt", "")
                    used_titles.add(title.lower())
                    # extract keywords
                    for arc_name, _ in ARCHITECTURE_POOL:
                        if arc_name.lower() in title.lower() or arc_name.lower() in prompt.lower():
                            used_architectures.add(arc_name)
                    for lnd_name, _ in LANDSCAPE_POOL:
                        if lnd_name.lower() in title.lower() or lnd_name.lower() in prompt.lower():
                            used_landscapes.add(lnd_name)
        except Exception:
            continue
            
    return used_titles, used_architectures, used_landscapes

def sample_weekday_portraits(n=3):
    """采样干净、独立、高质量摄影人像；不限定性别、年龄、族裔或风格。"""
    # 只接受可直接执行的摄影 Prompt，拒绝模板占位符、JSON/REFERENCE 工作流、多格版式和纯风景建筑。
    banned = ("{", "}", "<image", "--", "placeholder", "[", "]", "mirror", "镜面", "自拍", "selfie", "storyboard", "panel", "9-panel", "grid", "collage", "multipanel", "landscape photography", "magazine cover", " cover", "headline", "9:16", "16:9", "《", "》", "提示词", "制作了一组")
    import re as _re
    photo_cues = ("portrait", "photograph", "photography", "headshot", "cinematic portrait", "editorial portrait")
    human_cues = ("man", "woman", "person", "human", "face", "boy", "girl", "elder", "child", "adult", "青年", "女性", "男性", "portrait of", "portrait photography")
    human_re = _re.compile(r"\b(" + "|".join(_re.escape(c) for c in human_cues) + r")\b", _re.IGNORECASE)
    non_photo = ("robot", "android", "bugdroid", "notebook", "handwritten", "sketch", "illustration", "digital art", "3d render", "x-ray", "thermal scan", "product", "still life", "architecture", "mountain road", "landscape")
    candidates = []
    try:
        with open(DATA_PROMPTS_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        for item in data if isinstance(data, list) else []:
            if not isinstance(item, dict):
                continue
            title = str(item.get("title") or "Portrait").strip()
            prompt = str(item.get("prompt") or "").strip()
            low = prompt.lower()
            if len(prompt) < 120 or any(token in low for token in banned) or prompt.startswith("{"):
                continue
            if not any(cue in low for cue in photo_cues):
                continue
            if not human_re.search(prompt) or any(token in low for token in non_photo):
                continue
            # 排除明显无人建筑/风景和不适合直接执行的图形设计提示。
            if any(token in low for token in ("no people", "empty scene", "poster", "海报", "字体", "主标题", "advertisement", "banner", "layout", "editorial design", "graphic design", "product render", "器物", "中文", "landscape photography")):
                continue
            candidates.append((title, prompt))
    except (OSError, ValueError, TypeError):
        candidates = []

    # 先按题名和 Prompt 去重，再随机抽取；不向人物身份施加任何预设。
    unique = []
    seen = set()
    for title, prompt in candidates:
        key = " ".join(prompt.lower().split())
        if key not in seen:
            seen.add(key)
            unique.append((title, prompt))
    if len(unique) < n:
        unique.extend([
            ("Independent Portrait A", "High-end editorial portrait photography, an entirely independent subject chosen organically for the scene, natural expression, precise skin texture, cinematic light, medium-format camera, 85mm lens, shallow depth of field."),
            ("Independent Portrait B", "Museum-quality documentary portrait photography, an entirely independent subject chosen organically for the scene, authentic presence, nuanced natural light, honest skin texture, medium-format camera, 80mm lens."),
            ("Independent Portrait C", "Fine-art portrait photography, an entirely independent subject chosen organically for the scene, distinctive presence, controlled studio-cinematic lighting, crisp eyes, realistic skin texture, 90mm lens.")
        ])
    selected = random.sample(unique, n)
    diversity_clause = (
        " This is an independent portrait subject, not a recurring character and not a face copied from another image in this batch. "
        "Choose gender, age, ethnicity, facial structure, hair, styling and expression organically from the scene; impose no default beauty template and do not make the subjects look like the same person."
    )
    return [(title, prompt + diversity_clause) for title, prompt in selected]

def generate_batch(slot="am", target_date=None):
    now = datetime.datetime.now()
    if target_date:
        today_str = target_date
        weekday = datetime.datetime.strptime(target_date, "%Y-%m-%d").weekday()
    else:
        today_str = now.strftime("%Y-%m-%d")
        weekday = now.weekday()  # 0=Monday, 6=Sunday
        
    is_weekend = (weekday in [5, 6])
    run_id = f"{today_str}-{slot}"
    target_dir = os.path.join(VOLUMES_BASE, run_id)
    work_dir = os.path.join(target_dir, "work")
    os.makedirs(work_dir, exist_ok=True)
    
    used_titles, used_arcs, used_lnds = load_history_used_terms(30)
    
    batch = []
    
    if not is_weekend:
        # ===== 周一至周五工作日：前 3 张独立高级感人像 =====
        portraits = sample_weekday_portraits(3)
        for idx, (p_title, p_prompt) in enumerate(portraits, start=1):
            batch.append({
                "slot": f"0{idx}",
                "title": f"0{idx}-{p_title.lower().replace(' ', '-')}",
                "prompt": p_prompt,
                "negative_prompt": "ugly, deformed, bad anatomy, bad hands, missing fingers, extra fingers, blurry, plastic skin, oversaturated, watermark, signature",
                "aspect_ratio": "2:3",
                "mode": "text2img"
            })
    else:
        # ===== 周六周日周末：林晚拉鲁斯海报体系 =====
        batch.append({
            "slot": "01",
            "title": "01-linwan-larousse-poster",
            "prompt": "Authentic cinematic portrait of Lin Wan as a graceful young East Asian woman, dressed in modern minimalist off-white linen attire, neat low bun without stray bangs. Composition inspired by Larousse visual design: clean graphic lines framing the subject, authentic Chinese calligraphy title '静水流深' integrated harmoniously, soft museum exhibition gallery lighting, neutral warm grey textured background, shot on Hasselblad H6D-100c, 85mm lens, f/2.8, crisp authentic skin texture, natural soft catchlights, no beauty marks, no moles",
            "negative_prompt": "ugly, deformed, mole, beauty mark, bad eyes, bad hands, cartoon, 3d, cgi, plastic skin, messy hair, stray bangs",
            "aspect_ratio": "2:3",
            "mode": "text2img",
            "character": "Lin Wan",
            "identity_ref": "/Volumes/外接硬盘/hermes-images/daily-image-training/resources/linwan_f02_identity.png"
        })
        batch.append({
            "slot": "02",
            "title": "02-linwan-watercolor-clone",
            "prompt": "Masterpiece watercolor painting of the exact young East Asian woman from the reference image, strictly preserving identical facial features, narrow oval face, neat low bun hairstyle, and minimalist attire. Delicate translucent watercolor pigments on heavy cold-press cotton paper, subtle pigment bleeding and soft deckled edges, retaining pristine human anatomy, elegant painterly expression, authentic fine art painting",
            "negative_prompt": "photorealistic, photograph, 3d render, deformed face, wrong face, mole, beauty mark, high bun, different clothes, extra limbs, ugly, blurry",
            "aspect_ratio": "2:3",
            "mode": "img2img",
            "source_slot": "01"
        })
        batch.append({
            "slot": "03",
            "title": "03-linwan-lineart-clone",
            "prompt": "Masterpiece monochromatic Chinese Gongbi Bai Miao fine line ink drawing of the exact young East Asian woman from the reference image, strictly maintaining identical facial features, narrow oval face, neat low bun hairstyle, and minimalist attire. Pure black ink outlines on aged vintage Xuan paper, razor-sharp fluid calligraphy brush linework, zero color, zero heavy shading, clean minimalist negative space, traditional oriental fine art",
            "negative_prompt": "color, watercolor, photorealistic, photograph, 3d, deformed face, wrong face, mole, beauty mark, high bun, messy hair, heavy crosshatching, dirty paper",
            "aspect_ratio": "2:3",
            "mode": "img2img",
            "source_slot": "01"
        })

    # ===== 04-05 无人图；06-07 国风城市文旅海报（工作日与周末统一） =====
    # 04 著名建筑
    avail_arcs = [a for a in ARCHITECTURE_POOL if a[0] not in used_arcs]
    arc = random.choice(avail_arcs if avail_arcs else ARCHITECTURE_POOL)
    batch.append({
        "slot": "04",
        "title": f"04-{arc[0].lower().replace(' ', '-')}",
        "prompt": arc[1],
        "negative_prompt": "people, tourists, crowd, humans, watermark, blurry, deformed, cartoon, oversaturated",
        "aspect_ratio": "2:3",
        "mode": "text2img"
    })
    
    # 05 意境风景
    avail_lnds = [l for l in LANDSCAPE_POOL if l[0] not in used_lnds]
    lnd = random.choice(avail_lnds if avail_lnds else LANDSCAPE_POOL)
    batch.append({
        "slot": "05",
        "title": f"05-{lnd[0].lower().replace(' ', '-')}",
        "prompt": lnd[1],
        "negative_prompt": "people, tourists, man, woman, crowd, buildings, trash, watermark, cartoon",
        "aspect_ratio": "2:3",
        "mode": "text2img"
    })
    
    # 06 & 07 两座不同城市；优先排除30天内已经使用过的城市 slug。
    city_available = [c for c in CITY_POSTER_POOL if not any(c["slug"] in title for title in used_titles)]
    if len(city_available) < 2:
        city_available = CITY_POSTER_POOL
    city_selected = random.sample(city_available, 2)
    for slot_num, city_item in zip(("06", "07"), city_selected):
        batch.append({
            "slot": slot_num,
            "title": f"{slot_num}-{city_item['slug']}",
            "prompt": build_city_poster_prompt(city_item),
            "negative_prompt": "wrong landmark, mixed cities, inaccurate architecture, malformed hands, extra fingers, garbled text, letters, logo, watermark, giant face silhouette, double exposure, grid collage, hard photo frames, neon, plastic 3d render",
            "aspect_ratio": "2:3",
            "mode": "text2img",
            "style": "chinese-cultural-tourism-scroll-poster",
            "allow_people": True,
            "local_typography": {
                "city": city_item["city"],
                "english": city_item["english"],
                "main_title": city_item["title"],
                "seal": city_item["seal"],
                "placement": "left-30-percent-clean-column",
                "required": True
            }
        })
    
    # 写入当前场次预制配置
    batch_config_file = os.path.join(work_dir, "batch_plan.json")
    with open(batch_config_file, "w", encoding="utf-8") as f:
        json.dump({
            "run_id": run_id,
            "date": today_str,
            "is_weekend": is_weekend,
            "weekday_name": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][weekday],
            "total_images": len(batch),
            "items": batch
        }, f, indent=2, ensure_ascii=False)
        
    print(f"SUCCESS: Batch plan prepared in {batch_config_file}")
    print(f"Schedule: {'Weekend (Lin Wan Larousse + Clones)' if is_weekend else 'Weekday (3 Independent High-Aesthetic Portraits)'}")
    for item in batch:
        print(f"  [{item['slot']}] {item['title']} ({item['mode']})")
        
    return batch_config_file

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--slot", choices=["am", "pm"], default="am")
    parser.add_argument("--date", help="YYYY-MM-DD", default=None)
    args = parser.parse_args()
    generate_batch(slot=args.slot, target_date=args.date)
