import os

from constants import SORA_ACCESS_TOKEN
from sb_functions import *
from insta import upload_to_insta
from gist import *
import json,time
import requests
from video_post import post_to_sora


AUTH = f"Bearer {SORA_ACCESS_TOKEN}"

content = json.loads(get_gist_text())
prompt = content[0]
new_content = content[1:]

create_video = json.loads(create(AUTH=AUTH,prompt=prompt))

if(create_video["ok"]):
    print("Generating Video...")
    task_id=create_video["json"]["id"]
    time.sleep(300)
else:
    print(f"Some Error Occured : {create_video["status"]}")
    exit()

count = 3
isFound = False

while not isFound and count > 0:
    print(f"Checking drafts... (Attempt {4 - count}/3)")

    response = json.loads(get_drafs(AUTH=AUTH))

    all_video_links = response["json"]["items"]

    for item in all_video_links:
        item_id = item["task_id"]
        if item_id == task_id:
            # #new
            # gen_id,text = item.get("id"),item.get("prompt")
            # raw_result=post_to_sora(AUTH,text,gen_id)
            # data = json.loads(raw_result)
            # post_id = data["json"]["post"]["id"]

            # video_link=f"https://oscdn2.dyysy.com/MP4/{post_id}.mp4"

            video_link = item.get("downloadable_url")
            if video_link:
                print(f"Your video is ready: {video_link}")
                isFound = True
                break
            else:
                print("⏳ Task found but video not ready yet.")
                break
    else:
        print("Task not found in this attempt.")

    if not isFound:
        count -= 1
        if count > 0:
            print("Waiting 5 minutes before next check...")
            time.sleep(300)

if not isFound:
    print("Some error occurred or video not ready after 3 attempts.")
else:
    upload_to_insta(video_link)
    update_gist(json.dumps(new_content))
