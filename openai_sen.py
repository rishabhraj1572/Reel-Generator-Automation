from seleniumbase import SB
import json
import os
from datetime import datetime


def create_sentinel_values(headless=True):

    with SB(uc=True, test=True, locale="en", headless=headless) as sb:
        origin = "https://sora.chatgpt.com"
        print("🌐 Opening:", origin)
        sb.open(origin)
        sb.wait_for_ready_state_complete()
        sb.sleep(2)

        js_get_token = """
        const done = arguments[0];
        (async () => {
            try {
                if (!window.SentinelSDK || !window.SentinelSDK.token) {
                    done({ok:false, error:"SentinelSDK not found"});
                    return;
                }
                const result = await window.SentinelSDK.token("sora_2_create_task");
                let obj = result;
                try { if (typeof result === "string") obj = JSON.parse(result); } catch(e){}
                const { p, t, c } = obj || {};
                done({ok:true, p, t, c});
            } catch (err) {
                done({ok:false, error:String(err)});
            }
        })();
        """

        print("🔐 Extracting sentinel token...")
        token_data = sb.execute_async_script(js_get_token, timeout=90)

        if not token_data.get("ok"):
            raise RuntimeError(f"Token generation failed: {token_data.get('error')}")

        sentinel = {
            "p": token_data.get("p"),
            "t": token_data.get("t"),
            "c": token_data.get("c"),
        }

        os.makedirs("tokens", exist_ok=True)
        main_file = "tokens/sentinel_token.json"

        with open(main_file, "w") as f:
            json.dump(sentinel, f, indent=2)

        print(f"✅ Token extracted successfully:")
        print(json.dumps(sentinel, indent=2))
        print(f"💾 Saved to {main_file}")

        return sentinel

