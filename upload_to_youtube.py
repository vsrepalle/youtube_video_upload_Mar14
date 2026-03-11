#!/usr/bin/env python
# upload_to_youtube.py - Multi-Channel Production Edition
# Supports: Automatic channel detection from JSON & Separate Token Management

import os
import pickle
import json
import sys
import time
import logging
from pathlib import Path
from datetime import datetime

# Google API imports
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError

# ────────────────────────────────────────────────
#           LOGGING SETUP
# ────────────────────────────────────────────────
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)
log_file = log_dir / f"upload_{datetime.now().strftime('%Y%m%d')}.log"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)-7s | %(message)s',
    handlers=[logging.FileHandler(log_file), logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("YT_UPLOAD")

# If modifying these scopes, delete the specific channel's token.pickle.
SCOPES = ['https://www.googleapis.com/auth/youtube.upload',
          'https://www.googleapis.com/auth/youtube.force-ssl']

class YouTubeUploader:
    def __init__(self, client_secrets_file="client_secret.json"):
        self.client_secrets = client_secrets_file
        self.youtube = None
        self.active_channel = None
        
        if not Path(self.client_secrets).exists():
            logger.critical(f"Missing {self.client_secrets}! Get it from Google Cloud Console.")
            sys.exit(1)

    def get_authenticated_service(self, channel_name):
        """Manages separate tokens for each channel name."""
        # Sanitize channel name for filename
        safe_name = "".join([c for c in channel_name if c.isalnum()]).lower()
        token_file = Path(f"tokens/token_{safe_name}.pickle")
        token_file.parent.mkdir(exist_ok=True)

        creds = None
        if token_file.exists():
            with open(token_file, 'rb') as token:
                creds = pickle.load(token)

        # Refresh or Re-auth
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                logger.info(f"Refreshing access token for {channel_name}...")
                creds.refresh(Request())
            else:
                logger.info(f"New Authentication required for channel: {channel_name}")
                flow = InstalledAppFlow.from_client_secrets_file(self.client_secrets, SCOPES)
                creds = flow.run_local_server(port=0, prompt='consent')
            
            with open(token_file, 'wb') as token:
                pickle.dump(creds, token)

        self.active_channel = channel_name
        self.youtube = build('youtube', 'v3', credentials=creds)
        return True

    def perform_upload(self, video_path, data):
        """Handles the heavy lifting of the resumable upload."""
        # 1. Extract Meta from JSON
        headline = data.get('headline', 'New Short')
        details = data.get('details', '')
        sub_hook = data.get('subscribe_hook', '')
        meta = data.get('metadata', {})
        
        # 2. Build Description
        description = f"{headline}\n\n{details}\n\n{sub_hook}\n\n"
        description += " ".join(meta.get('hashtags', []))
        
        body = {
            'snippet': {
                'title': headline[:100],
                'description': description[:5000],
                'tags': meta.get('tags', [])[:20],
                'categoryId': '22' # People & Blogs
            },
            'status': {
                'privacyStatus': 'private', # Always start private for safety
                'selfDeclaredMadeForKids': False
            }
        }

        # 3. Initialize Media Upload
        logger.info(f"Initializing upload for: {video_path.name}")
        media = MediaFileUpload(
            str(video_path), 
            mimetype='video/mp4', 
            chunksize=1024*1024, 
            resumable=True
        )

        try:
            request = self.youtube.videos().insert(
                part=','.join(body.keys()),
                body=body,
                media_body=media
            )

            response = None
            while response is None:
                status, response = request.next_chunk()
                if status:
                    progress = int(status.progress() * 100)
                    print(f" > [{self.active_channel}] Uploading: {progress}% complete", end='\r')
            
            logger.info(f"✅ SUCCESS! Video ID: {response['id']} on {self.active_channel}")
            return response['id']

        except HttpError as e:
            logger.error(f"HTTP Error: {e.resp.status} - {e.content}")
        except Exception as e:
            logger.error(f"Unexpected error during upload: {e}")
        return None

def main():
    # Setup
    uploader = YouTubeUploader()
    
    # 1. Find Latest Video
    output_dir = Path("output")
    videos = list(output_dir.glob("*.mp4"))
    if not videos:
        logger.error("No videos found in output/"); return
    latest_video = max(videos, key=lambda p: p.stat().st_ctime)

    # 2. Load Metadata (data.json)
    json_path = Path("data.json")
    if not json_path.exists():
        logger.error("data.json not found!"); return
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 3. Switch Channel based on JSON
    target_channel = data.get('channel', 'DefaultChannel')
    logger.info(f"Detecting target channel: {target_channel}")
    
    # Authenticate (This opens browser ONLY if no token exists for THIS channel)
    uploader.get_authenticated_service(target_channel)

    # 4. Final Confirmation
    print(f"\nTarget: {target_channel}")
    print(f"Video: {latest_video.name}")
    confirm = input("Proceed with upload? (y/n): ").lower()
    
    if confirm == 'y':
        uploader.perform_upload(latest_video, data)
    else:
        logger.info("Upload cancelled by user.")

if __name__ == "__main__":
    main()