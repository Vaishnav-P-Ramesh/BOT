# upload_to_youtube.py
import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def upload_video(file_path, title, description="Uploaded via Discord bot", categoryId="22", privacyStatus="unlisted"):
    creds = None

    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", SCOPES)
        creds = flow.run_local_server(port=0)
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    youtube = build("youtube", "v3", credentials=creds)

    request_body = {
        "snippet": {
            "categoryId": categoryId,
            "title": title,
            "description": description
            

        },
        "status": {
           "privacyStatus": "public",  # Upload as PUBLIC
            "selfDeclaredMadeForKids": False
        }
    }

    media = MediaFileUpload(file_path)
    response = youtube.videos().insert(
        part="snippet,status",
        body=request_body,
        media_body=media
    ).execute()

    return response.get("id")
