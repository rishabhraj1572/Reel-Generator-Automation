import json
import os
from seleniumbase import SB
from constants import SORA_ACCESS_TOKEN, SORA_CHATGPT_ID
from openai_sen import create_sentinel_values

AUTH= f"Bearer {SORA_ACCESS_TOKEN}"
def post_to_sora(AUTH, post_text, generation_id):
    SENTINEL_TOKEN = create_sentinel_values()
    SENTINEL_TOKEN.update({
        "id": f"{SORA_CHATGPT_ID}", #Your Sora/ChatGPT id here
        "flow": "sora_2_create_task"
    })
    payload = {
        "attachments_to_create": [
            {"generation_id": generation_id, "kind": "sora"}
        ],
        "post_text": post_text
    }

    url = "https://sora.chatgpt.com/backend/project_y/post"
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
            try {{ text = await r.text(); }} catch(e) {{ text = String(e); }}
            let parsed = null;
            try {{ parsed = JSON.parse(text); }} catch(e) {{ parsed = null; }}
            callback({{status: r.status, ok: r.ok, text: text, json: parsed}});
        }})
        .catch(err => {{
            callback({{error: String(err)}});
        }});
        """

        result = sb.execute_async_script(js_async)

        # Optional helper to save output
        with open("sora_post_response.json", "w") as f:
            json.dump(result, f, indent=2)

        print(json.dumps(result, indent=2)[:2000])
        return json.dumps(result, indent=2)

