import requests
import time

from constants import ACCESS_TOKEN, IG_USER_ID, CAPTION

def upload_to_insta(VIDEO_URL):

    create_url = f"https://graph.facebook.com/v24.0/{IG_USER_ID}/media"
    payload = {
        "media_type": "REELS",
        "video_url": VIDEO_URL,
        "caption": CAPTION,
        "access_token": ACCESS_TOKEN
    }

    r = requests.post(create_url, data=payload)
    media_data = r.json()

    if "error" in media_data:
        print("Error creating media container:", media_data["error"])
        exit()

    CREATION_ID = media_data["id"]
    print(f"Media container created: {CREATION_ID}")

    status_url = f"https://graph.facebook.com/v24.0/{CREATION_ID}?fields=status_code&access_token={ACCESS_TOKEN}"
    status = ""
    while status != "FINISHED":
        time.sleep(5)  # wait 5 seconds
        r = requests.get(status_url)
        status_data = r.json()
        status = status_data.get("status_code", "")
        print(f"Media status: {status}")

    publish_url = f"https://graph.facebook.com/v24.0/{IG_USER_ID}/media_publish"
    payload = {
        "creation_id": CREATION_ID,
        "access_token": ACCESS_TOKEN
    }

    r = requests.post(publish_url, data=payload)
    publish_data = r.json()

    if "error" in publish_data:
        print("Error publishing Reel:", publish_data["error"])
    else:
        print("Reel published successfully! ID:", publish_data.get("id"))

