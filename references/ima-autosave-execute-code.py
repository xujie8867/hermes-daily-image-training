# IMA 7-step auto-save: upload image + prompt to King knowledge base
# Run via execute_code. Uses subprocess.run with argument lists to avoid shell escaping issues.
# KB_ID for King: Jd-PS6UrDkJDUV7pqFj770VeO0e81s8JAW2tnj5DygI=

from hermes_tools import terminal, read_file
import json, os, subprocess

SKILL_DIR = "/Users/xuhailong/.hermes/skills/ima-skill"
KB_ID = "Jd-PS6UrDkJDUV7pqFj770VeO0e81s8JAW2tnj5DygI="
IMAGE_PATH = "/path/to/image.png"  # REPLACE ME
HOME = "/Users/xuhailong"

client_id = open(f"{HOME}/.config/ima/client_id").read().strip()
api_key = open(f"{HOME}/.config/ima/api_key").read().strip()
opts_json = json.dumps({"clientId": client_id, "apiKey": api_key})

def ima_api(api_path, body_obj):
    body = json.dumps(body_obj)
    cmd = ["node", f"{SKILL_DIR}/ima_api.cjs", api_path, body, opts_json]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    if result.returncode != 0:
        raise Exception(f"IMA API error [{api_path}]: {result.stderr.strip()}")
    resp = json.loads(result.stdout)
    if resp.get("code") != 0:
        raise Exception(f"IMA business error [{api_path}]: {resp.get('msg')}")
    return resp

# Step 1: preflight
preflight = subprocess.run(
    ["node", f"{SKILL_DIR}/knowledge-base/scripts/preflight-check.cjs", "--file", IMAGE_PATH],
    capture_output=True, text=True, timeout=30
)
pf = json.loads(preflight.stdout)
if not pf.get("pass"):
    raise Exception(f"Preflight failed: {pf.get('reason')}")

# Step 2: create_media
create_resp = ima_api("openapi/wiki/v1/create_media", {
    "file_name": pf["file_name"], "file_size": pf["file_size"],
    "content_type": pf["content_type"], "knowledge_base_id": KB_ID,
    "file_ext": pf["file_ext"]
})
media_id = create_resp["data"]["media_id"]
cos_cred = create_resp["data"]["cos_credential"]

# Step 3: COS upload (CRITICAL: use argument list, never shell string)
upload_result = subprocess.run(
    ["node", f"{SKILL_DIR}/knowledge-base/scripts/cos-upload.cjs",
     "--file", IMAGE_PATH,
     "--secret-id", cos_cred["secret_id"],
     "--secret-key", cos_cred["secret_key"],
     "--token", cos_cred["token"],
     "--bucket", cos_cred["bucket_name"],
     "--region", cos_cred["region"],
     "--cos-key", cos_cred["cos_key"],
     "--content-type", pf["content_type"],
     "--start-time", str(cos_cred["start_time"]),
     "--expired-time", str(cos_cred["expired_time"]),
     "--timeout", "300000"],
    capture_output=True, text=True, timeout=120
)
if upload_result.returncode != 0:
    raise Exception(f"COS upload failed: {upload_result.stderr}")

# Step 4: add_knowledge (media_type=9, image)
ima_api("openapi/wiki/v1/add_knowledge", {
    "media_type": pf["media_type"], "media_id": media_id,
    "title": pf["file_name"], "knowledge_base_id": KB_ID,
    "file_info": {"cos_key": cos_cred["cos_key"], "file_size": pf["file_size"], "file_name": pf["file_name"]}
})

# Step 5: get_media_info (get IMA-hosted URL)
media_info = ima_api("openapi/wiki/v1/get_media_info", {"media_id": media_id})
ima_url = media_info["data"].get("url_info", {}).get("url", "")

# Step 6: import_doc (create note with image URL + prompt)
# NOTE_TITLE and NOTE_CONTENT must be set before this step
note_resp = ima_api("openapi/note/v1/import_doc", {
    "content_format": 1,
    "content": NOTE_CONTENT  # Markdown with ![image](ima_url) + prompt text
})
note_id = note_resp["data"]["note_id"]

# Step 7: add_knowledge (media_type=11, note)
ima_api("openapi/wiki/v1/add_knowledge", {
    "media_type": 11,
    "note_info": {"content_id": note_id},
    "title": NOTE_TITLE,
    "knowledge_base_id": KB_ID
})

print(f"DONE: image={media_id}, note={note_id}")
