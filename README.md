
**Project Overview**
- **Name**: Reel Generator Automation
- **Description**: This project automates the entire pipeline of generating and publishing Instagram Reels using a list of prompts. Simply provide your prompts, and the system will automatically create reels, render them, and upload them to Instagram—without any manual effort.

With Docker support, you can easily schedule and run the workflow at any time. Just load your prompts, and the automated pipeline will handle everything from content generation to final publishing.

Perfect for content creators, agencies, and automated social media workflows.

**Quick Features**
- **Content scripts**: run discrete scripts to create and post content.
- **Social posting**: helpers for posting to Instagram.
- **OpenAI integration**: utilities to call OpenAI model Sora.
- **Project constants**: centralized configuration in `constants.py`.
- **Pipeline automation**: automates end-to-end generation of Instagram Reels from a list of prompts and publishes them.

**Repository Layout**
- **`sora.py`**: Main script (entry point for combined workflows).
- **`insta.py`**: Instagram posting utilities.
- **`video_post.py`**: Video creation / posting helpers.
- **`gist.py`**: Create and publish GitHub Gists.
- **`openai_sen.py`**: OpenAI-related utilities.
- **`sb_functions.py`**: Shared helper functions used across scripts.
- **`constants.py`**: Place to set API keys, tokens, and other configuration values.
- **`requirements.txt`**: Python dependencies.
- **`Dockerfile`**: Container build recipe for running the project in Docker.

**Requirements**
- **Python**: 3.8+ recommended.
- Install dependencies:

```bash
python -m pip install -r requirements.txt
```

**Configuration**
- Edit `constants.py` with your credentials and keys, and follow the steps below to obtain required tokens and IDs.

**Steps to Follow**

1. Create the `video_prompt` Gist
	- Go to https://gist.github.com/ and create a new gist named `video_prompt`.
	- Now Add your video generation prompts in an array. Ex. ['proompt1','prompt2']
	- After saving, copy the Gist ID from the URL: `https://gist.github.com/<username>/<GIST_ID>` — keep the `<GIST_ID>` value.
	- Add `GIST_ID` to `constants.py` (or export it as an environment variable).

2. Create a GitHub token with `gist` permission
	- Open https://github.com/settings/tokens (or https://github.com/settings/tokens/new for classic tokens).
	- Create a Personal Access Token and enable the `gist` scope (and any other scopes you need).
	- Copy the token and store it in `constants.py` as `GITHUB_TOKEN`, or set it as `GITHUB_TOKEN` in your environment.

3. Obtain a Facebook Graph API Access Token for an Instagram-connected Page
	- Ensure your Instagram account is a Business or Creator account and is connected to a Facebook Page.
	- Create an app in the Facebook Developer dashboard: https://developers.facebook.com/.
	- Add **Instagram Basic Display** / **Instagram Graph API** and configure the app.
	- Use the Graph API Explorer or the OAuth flow to generate a Page access token for the Facebook Page connected to your Instagram account. The token should include permissions such as `pages_show_list`, `instagram_basic`, and `instagram_content_publish`.
	- Use the Graph API Explorer or the OAuth flow to generate a short-lived user access token.
	- Exchange a short-lived user token for a long-lived user token by calling the Facebook OAuth exchange endpoint. Example (replace `APP_ID`, `APP_SECRET`, and `SHORT_LIVED_TOKEN`):

	```bash
	curl -X GET "https://graph.facebook.com/v16.0/oauth/access_token?grant_type=fb_exchange_token&client_id=APP_ID&client_secret=APP_SECRET&fb_exchange_token=SHORT_LIVED_TOKEN"
	```

	- The response will include `access_token` for the Page — use that as your `ACCESS_TOKEN` in `constants.py`.

4. Get the Instagram Business/Creator Account numeric ID (`IG_USER_ID`)
	- `IG_USER_ID` is NOT your Instagram username. It is the numeric Instagram account ID for a Business/Creator account.
	- Retrieve it via the Graph API: GET `/{page-id}?fields=connected_instagram_account` or use the Facebook Developer tools when the Instagram account is connected to the Page.
	- Add the numeric ID to `constants.py` as `IG_USER_ID`.

5. Get ChatGPT / Sora session token and ID
	- Log in to your ChatGPT / Sora account in the browser.
	- While logged in, open: `https://chatgpt.com/api/auth/session` — this returns session JSON containing tokens and identifiers.
	- Copy the 'accessToken' and the 'account->id' fields you need and add them to `constants.py` as `SORA_ACCESS_TOKEN` and `SORA_CHATGPT_ID`.
	- IMPORTANT: You must have generated at least one video in the new Sora version at `sora.chatgpt.com` (the new Sora UI) before video endpoints will work with these tokens.

6. Update `constants.py` with these keys.



**Usage Examples**
- Run the main script:

```bash
python sora.py
```

- Create a gist:

```bash
python gist.py --file snippet.py --title "Snippet"
```

**Docker**
- Build the image:

```bash
docker buildx build --platform linux/amd64 -t sora:latest .
```

**Contributing**
- Open an issue or a pull request with a clear description of bug fixes or features.
- Keep changes focused and add tests where appropriate.
# Reel-Generator-Automation
