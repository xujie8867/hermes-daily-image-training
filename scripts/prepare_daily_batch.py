#!/usr/bin/env python3
"""
prepare_daily_batch.py - 每日生图前置批处理准备脚本 (v1.0.0)
功能：
1. 3秒内完成过去30天历史生成去重（建筑、风景、人像题材）。
2. 根据当天是周几自动分流：
   - 周一至周五：01-03 从词库采样3条独立顶级人像Prompt（不限林晚、不限风格）；
   - 周六周日：01固定林晚拉鲁斯海报，02/03做1:1水彩与线稿复刻配置；
   - 04-07：建筑、风景、自由方向A、自由方向B（严格排除30天历史）。
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

# 自由方向池
FREE_TOPICS_POOL = [
    ("Antarctic Emperor Penguin", "A solitary Emperor penguin standing on pristine Antarctic sea ice beside deep sapphire iceberg walls, low angle golden hour sunlight illuminating delicate orange-gold neck plumage, crisp subzero atmospheric clarity, telephoto wildlife shot 400mm f/4, ultra-realistic texture"),
    ("Pine Needle Dewdrop Macro", "Macro extreme close-up of a solitary spherical dewdrop suspended on the tip of a fresh green pine needle, perfectly refracting an entire morning pine forest and rising golden sun inside the water sphere, razor-thin depth of field, 100mm macro f/2.8"),
    ("Deep Sea Bioluminescent Jellyfish", "A solitary translucent Aequorea victoria jellyfish drifting in abyssal midnight ocean, pulsating with ethereal neon-cyan and indigo bioluminescence, delicate trailing tentacles, pitch black deep water, macro wildlife photography, ultra sharp"),
    ("Sahara Fennec Fox", "A delicate cream-colored Fennec fox resting on wind-sculpted desert sand dune at sunset, huge alert translucent ears catching warm amber light, soft fine fur textures, low angle telephoto portrait 300mm f/2.8")
]

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
    """从 all-prompts.json 采样 3 条高质量独立人像 Prompt"""
    if not os.path.exists(DATA_PROMPTS_PATH):
        # 降级备用
        return [
            ("Indie Bookstore Portrait", "Cinematic portrait of a contemplative young woman in an indie bookstore, warm tungsten ambient light spilling between vintage wooden shelves, natural unposed expression, shot on Leica M11, 50mm f/1.4, film grain, photorealistic skin texture, 8k"),
            ("Rooftop Sunset Editorial", "Fashion editorial portrait of a woman standing on an urban rooftop at golden sunset, soft breeze catching silk jacket, low angle perspective against warm glowing city skyline, Sony A7R V, 85mm f/1.4, soft lens flare, crisp eyes, authentic skin tones"),
            ("Seaside Golden Hour", "Atmospheric documentary portrait of a young woman by the sea at twilight, ocean spray mist, subtle windblown hair, soft warm twilight backlight, Canon EOS R5, 85mm f/1.2, shallow depth of field, honest natural gaze, cinematic realism")
        ][:n]
        
    try:
        with open(DATA_PROMPTS_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        portrait_candidates = []
        for item in data:
            if isinstance(item, dict):
                cat = item.get("category", "").lower()
                prompt = item.get("prompt", "")
                title = item.get("title", "")
                if cat == "portrait" or "portrait" in prompt.lower() or "woman" in prompt.lower() or "man" in prompt.lower():
                    portrait_candidates.append((title or "Portrait", prompt))
        if len(portrait_candidates) >= n:
            selected = random.sample(portrait_candidates, n)
            return selected
    except Exception:
        pass
        
    return [
        ("Indie Bookstore Portrait", "Cinematic documentary portrait of a young woman in an indie bookstore stairwell, muted cool ambient tones, authentic skin textures, Hasselblad 80mm f/2.8, natural light"),
        ("Rooftop Golden Hour", "Contemporary streetwear portrait of a young woman on an industrial rooftop at sunset, warm cinematic backlighting, shallow depth of field, Sony A1 85mm f/1.4"),
        ("Seaside Twilight Portrait", "Moody cinematic portrait of a woman standing on a windswept coastline at dusk, subtle waves bokeh, Kodak Portra 400 aesthetic, crisp details")
    ][:n]

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

    # ===== 04-07 无人图（工作日与周末统一） =====
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
    
    # 06 & 07 自由方向
    free_selected = random.sample(FREE_TOPICS_POOL, 2)
    batch.append({
        "slot": "06",
        "title": f"06-{free_selected[0][0].lower().replace(' ', '-')}",
        "prompt": free_selected[0][1],
        "negative_prompt": "people, human, ugly, blurry, deformed, cartoon, signature, text",
        "aspect_ratio": "2:3",
        "mode": "text2img"
    })
    batch.append({
        "slot": "07",
        "title": f"07-{free_selected[1][0].lower().replace(' ', '-')}",
        "prompt": free_selected[1][1],
        "negative_prompt": "people, human, ugly, blurry, deformed, cartoon, signature, text",
        "aspect_ratio": "2:3",
        "mode": "text2img"
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
