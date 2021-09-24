import os
from googleapiclient.discovery import build
import base64
import requests
import time

# Setting up access tokens
# spotify tokens
CLIENT_ID = os.environ.get('spotify_client_id')
CLIENT_SECRET = os.environ.get('spotify_client_secret')
authorise_url = "https://accounts.spotify.com/authorize"
TOKEN_URL = 'https://accounts.spotify.com/api/token'
# gcp tokens
yt_id = os.environ.get('yt_id')
yt_secret = os.environ.get('yt_secret')
google_token = os.environ.get('google_token')
yt_scopes = ["https://www.googleapis.com/auth/youtube"]
# youtube data api v3 token
yt_api_key = os.environ.get('yt_api_key')


# Spotify authorisation
def authorise():
    token_url = "https://accounts.spotify.com/api/token"
    token_params = {"grant_type": "client_credentials"}
    client_creds = f"{CLIENT_ID}:{CLIENT_SECRET}"
    headers = {"Authorization": f"Basic {base64.b64encode(client_creds.encode()).decode()}"}
    res = requests.post(token_url, data=token_params, headers=headers)
    return res.json()


def get_playlist_tracks(access_token, playlist_id):
    playlist_url = f"https://api.spotify.com/v1/playlists/{playlist_id}"
    headers = {"Authorization": f"Bearer {access_token}"}
    r = requests.get(playlist_url, headers=headers)
    tracks_items = r.json()["tracks"]["items"]
    global name_artist
    name_artist = []
    for track in tracks_items:
        name = track["track"]["name"] + ","

        artists = ""
        # print("Track:", track["track"]["name"])
        for artist in track["track"]["artists"]:
            # artists.append(artist["name"])
            artists += str(artist["name"]) + ","

        name_artist.append(name + artists)


if __name__ == '__main__':
    token = authorise()["access_token"]
    get_playlist_tracks(token, "6T2nXNSsfN4tIBdfQGtBbc")


def get_youtube_playlist():
    playlist_link = "http://www.youtube.com/watch_videos?video_ids="
    for name in name_artist:
        youtube = build("youtube", "v3", developerKey=yt_api_key)
        request = youtube.search().list(
            part="snippet",
            q=name,
            maxResults=1)
        response = request.execute()
        playlist_link += response['items'][0]["id"]["videoId"] + ","
        time.sleep(1)
    return playlist_link