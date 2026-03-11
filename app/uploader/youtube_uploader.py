"""YouTube upload with OAuth flow"""

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError
import config
import os
from pathlib import Path

# Optional: store token once authenticated (speeds up repeated runs)
TOKEN_PATH = Path("temp/youtube_token.json")

def get_authenticated_service():
    """Authenticate once and reuse token if available"""
    credentials = None

    if TOKEN_PATH.exists():
        from google.oauth2.credentials import Credentials
        credentials = Credentials.from_authorized_user_file(TOKEN_PATH, config.YOUTUBE_SCOPES)

    if not credentials or not credentials.valid:
        flow = InstalledAppFlow.from_client_secrets_file(
            config.YOUTUBE_CLIENT_SECRETS_FILE,
            scopes=config.YOUTUBE_SCOPES
        )
        credentials = flow.run_local_server(port=0)

        # Save token for next time
        with open(TOKEN_PATH, 'w') as token_file:
            token_file.write(credentials.to_json())

    return build("youtube", "v3", credentials=credentials)


def upload_video(
    video_path: str,
    title: str,
    description: str,
    tags: list[str] | None = None,
    category_id: str = "27",          # Education (good default for facts/shorts)
    privacy_status: str = "private",  # safer default during development
) -> str | None:
    """
    Upload video to YouTube.
    Returns video ID on success, None on failure.
    """
    if not Path(video_path).is_file():
        print(f"❌ Video file not found: {video_path}")
        return None

    try:
        youtube = get_authenticated_service()
    except Exception as e:
        print(f"❌ Authentication failed: {e}")
        return None

    body = {
        "snippet": {
            "title": title[:100],           # YouTube title limit
            "description": description[:5000],
            "tags": tags or [],
            "categoryId": category_id
        },
        "status": {
            "privacyStatus": privacy_status
        }
    }

    media = MediaFileUpload(video_path, chunksize=-1, resumable=True)

    try:
        print(f"Uploading: {title}")
        request = youtube.videos().insert(
            part="snippet,status",
            body=body,
            media_body=media
        )

        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                print(f"  Progress: {int(status.progress() * 100)}%")

        video_id = response['id']
        print(f"✅ Upload complete!")
        print(f"   Video ID: {video_id}")
        print(f"   Link:    https://youtu.be/{video_id}")
        print(f"   Privacy: {privacy_status}")
        return video_id

    except HttpError as e:
        print(f"❌ YouTube API error: {e.resp.status} - {e.content}")
        return None
    except Exception as e:
        print(f"❌ Unexpected upload error: {e}")
        return None