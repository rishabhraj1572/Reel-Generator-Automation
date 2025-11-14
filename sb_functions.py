import json,os
from seleniumbase import SB
from time import sleep
from datetime import datetime
from constants import SORA_CHATGPT_ID
from openai_sen import create_sentinel_values



SENTINEL_TOKEN = create_sentinel_values()
SENTINEL_TOKEN.update({
    "id": f"{SORA_CHATGPT_ID}",
    "flow": "sora_2_create_task"
})


def save_json(filename, data):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def create(AUTH, prompt):
    payload = {
        "kind": "video",
        "prompt": f"{prompt}",
        "title": None,
        "orientation": "portrait",
        "size": "small",
        "n_frames": 600,
        "inpaint_items": [],
        "remix_target_id": None,
        "cameo_ids": None,
        "cameo_replacements": None,
        "model": "sy_8",
        "style_id": None,
        "audio_caption": None,
        "audio_transcript": None,
        "video_caption": None,
        "storyboard_id": None,
    }

    url = "https://sora.chatgpt.com/backend/nf/create"
    origin = "https://sora.chatgpt.com"

    with SB(uc=True, test=True, locale="en", headless=True) as sb:
        sb.open(origin)
        sb.sleep(1)

        js_async = f"""
        const callback = arguments[arguments.length - 1];
        const url = "{url}";
        const payload = {json.dumps(payload)};
        const auth = "{AUTH}";
        const sentinel = {json.dumps(SENTINEL_TOKEN)};

        fetch(url, {{
            method: 'POST',
            headers: {{
                'Authorization': auth,
                'Content-Type': 'application/json',
                'openai-sentinel-token': JSON.stringify(sentinel)
            }},
            body: JSON.stringify(payload)
        }})
        .then(async r => {{
            let text;
            try {{ text = await r.text(); }} catch(e){{ text = String(e); }}
            let parsed = null;
            try {{ parsed = JSON.parse(text); }} catch(e) {{ parsed = null; }}
            callback({{status: r.status, ok: r.ok, text: text, json: parsed}});
        }})
        .catch(err => {{
            callback({{error: String(err)}});
        }});
        """

        result = sb.execute_async_script(js_async)
        save_json("sora_response.json", result)
        print(json.dumps(result, indent=2)[:2000])
        return json.dumps(result, indent=2)


def create1(AUTH, prompt):
    payload = {
        "kind": "video",
        "prompt": prompt,
        "title": None,
        "orientation": "portrait",
        "size": "small",
        "n_frames": 600,
        "inpaint_items": [],
        "remix_target_id": None,
        "cameo_ids": None,
        "cameo_replacements": None,
        "model": "sy_8",
        "style_id": None,
        "audio_caption": None,
        "audio_transcript": None,
        "video_caption": None,
        "storyboard_id": None,
    }

    url = "https://sora.chatgpt.com/backend/nf/create"
    origin = "https://sora.chatgpt.com"

    with SB(uc=True, test=True, locale="en", headless=False) as sb:
        print("🌐 Opening browser and loading Sora origin...")
        sb.open(origin)
        sb.sleep(2)  # allow page + SDK load

        # STEP 1: Ensure SentinelSDK is present
        sdk_found = sb.execute_script("return typeof window.SentinelSDK !== 'undefined';")
        if not sdk_found:
            raise Exception("⚠️ SentinelSDK not found — ensure the target page loads it.")

        # STEP 2: Generate a legitimate openai-sentinel-token
        print("🔄 Generating openai-sentinel-token (may take a few seconds)...")
        js_token = """
        const done = arguments[0];
        (async () => {
            try {
                if (!window.SentinelSDK || !window.SentinelSDK.token) {
                    done({ok:false, error:"SentinelSDK.token() not available"});
                    return;
                }
                const tokenValue = await window.SentinelSDK.token("chat-requirement");
                done({ok:true, token: tokenValue});
            } catch (err) {
                done({ok:false, error:String(err)});
            }
        })();
        """

        sentinel_result = sb.execute_async_script(js_token, timeout=120000)
        if not sentinel_result.get("ok"):
            raise Exception(f"Sentinel token generation failed: {sentinel_result.get('error')}")

        SENTINEL_TOKEN = sentinel_result["token"]
        print("✅ Generated openai-sentinel-token:")
        print(SENTINEL_TOKEN[:150] + "...")

        # STEP 3: Perform authorized POST request with the live token
        js_async = f"""
        const callback = arguments[arguments.length - 1];
        const url = "{url}";
        const payload = {json.dumps(payload)};
        const auth = "{AUTH}";
        const sentinel = "{SENTINEL_TOKEN}";

        fetch(url, {{
            method: 'POST',
            headers: {{
                'Authorization': auth,
                'Content-Type': 'application/json',
                'openai-sentinel-token': sentinel
            }},
            body: JSON.stringify(payload)
        }})
        .then(async r => {{
            let text;
            try {{ text = await r.text(); }} catch(e){{ text = String(e); }}
            let parsed = null;
            try {{ parsed = JSON.parse(text); }} catch(e) {{ parsed = null; }}
            callback({{status: r.status, ok: r.ok, text: text, json: parsed}});
        }})
        .catch(err => {{
            callback({{error: String(err)}});
        }});
        """

        print("🚀 Sending request to backend...")
        result = sb.execute_async_script(js_async, timeout=120000)

        # --- STEP 4: Save results to two files ---
        os.makedirs("responses", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        main_file = f"responses/sora_response.json"
        backup_file = f"responses/sora_response_{timestamp}.json"

        with open(main_file, "w") as f:
            json.dump(result, f, indent=2)

        with open(backup_file, "w") as f:
            json.dump(result, f, indent=2)

        print(f"\n💾 Response saved to:")
        print(f" - {main_file}")
        print(f" - {backup_file}\n")

        print("🔹 Response Preview:")
        print(json.dumps(result, indent=2)[:2000])

        return result



def get_drafs(AUTH):
    url = "https://sora.chatgpt.com/backend/project_y/profile/drafts?limit=15"
    origin = "https://sora.chatgpt.com"

    with SB(uc=True, test=True, locale="en", headless=True) as sb:
        sb.open(origin)
        sb.sleep(1)

        js_async = f"""
        const callback = arguments[arguments.length - 1];
        const url = "{url}";
        const auth = "{AUTH}";
        const sentinel = {json.dumps(SENTINEL_TOKEN)};

        fetch(url, {{
            method: 'GET',
            headers: {{
                'Authorization': auth,
                'Content-Type': 'application/json',
                'openai-sentinel-token': JSON.stringify(sentinel)
            }}
        }})
        .then(async r => {{
            let text;
            try {{ text = await r.text(); }} catch(e){{ text = String(e); }}
            let parsed = null;
            try {{ parsed = JSON.parse(text); }} catch(e) {{ parsed = null; }}
            callback({{status: r.status, ok: r.ok, text: text, json: parsed}});
        }})
        .catch(err => {{
            callback({{error: String(err)}});
        }});
        """

        result = sb.execute_async_script(js_async)
        save_json("sora_response_get.json", result)
        print(json.dumps(result, indent=2)[:2000])
        return json.dumps(result, indent=2)
    

