import requests,json
from constants import GIST_ID, GITHUB_TOKEN

FILE_NAME = "video_prompt"

HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}

def update_gist(text: str):
    url = f"https://api.github.com/gists/{GIST_ID}"
    payload = {
        "files": {
            FILE_NAME: {
                "content": text
            }
        }
    }
    response = requests.patch(url, headers=HEADERS, json=payload)
    if response.status_code == 200:
        print("Gist updated successfully!")
    else:
        print("Error updating gist:", response.json())

def get_gist_text():
    url = f"https://api.github.com/gists/{GIST_ID}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        files = response.json().get("files", {})
        return files.get(FILE_NAME, {}).get("content", "")
    else:
        print("Error fetching gist:", response.json())
        return None

