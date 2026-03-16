import os
import sys
import pickle
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from googleapiclient.http import MediaFileUpload
import json

# --- CONFIGURATION ---
CLIENT_SECRETS_FILE = "client_secrets.json"
TOKEN_FILE = "token.pickle"
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def get_authenticated_service():
    credentials = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            credentials = pickle.load(token)
    
    if not credentials or not credentials.valid:
        if not os.path.exists(CLIENT_SECRETS_FILE):
            print(f"❌ Error: {CLIENT_SECRETS_FILE} not found. Please download it from Google Cloud Console.")
            sys.exit(1)
        
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
        credentials = flow.run_local_server(port=0)
        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(credentials, token)

    return googleapiclient.discovery.build("youtube", "v3", credentials=credentials)

def upload_video():
    # 1. Find the latest video in the output folder
    output_dir = "output"
    videos = [os.path.join(output_dir, f) for f in os.listdir(output_dir) if f.endswith(".mp4")]
    if not videos:
        print("❌ No videos found in output folder.")
        return
    
    latest_video = max(videos, key=os.path.getctime)
    
    # 2. Get metadata from data.json
    try:
        with open("data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            meta = data.get("metadata", {})
            title = meta.get("title", "New TrendWave Short")
            description = meta.get("description", "Uploaded via TrendWave Automation")
            tags = meta.get("hashtags", [])
    except:
        title, description, tags = "New TrendWave Short", "", []

    print(f"🚀 Uploading: {latest_video}...")
    youtube = get_authenticated_service()

    request_body = {
        "snippet": {
            "title": title[:100],
            "description": description,
            "tags": tags,
            "categoryId": "22" # People & Blogs
        },
        "status": {
            "privacyStatus": "private", # As per user preference
            "selfDeclaredMadeForKids": False
        }
    }

    media = MediaFileUpload(latest_video, chunksize=-1, resumable=True)
    request = youtube.videos().insert(part="snippet,status", body=request_body, media_body=media)

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"   → Uploaded {int(status.progress() * 100)}%")

    print(f"✅ Video Uploaded! Video ID: {response['id']}")

if __name__ == "__main__":
    upload_video()
