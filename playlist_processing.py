import base64
import os
import requests
from googleapiclient.discovery import build

# Setting up access tokens
# spotify tokens
client_id = os.environ.get('spotify_client_id')
client_secret = os.environ.get('spotify_client_secret')
authorise_url = "https://accounts.spotify.com/authorize"
token_url = 'https://accounts.spotify.com/api/token'
# gcp tokens
yt_id = os.environ.get('yt_id')
yt_secret = os.environ.get('yt_secret')
yt_scopes = ["https://www.googleapis.com/auth/youtube"]
# youtube data api v3 token
yt_api_key = os.environ.get('yt_api_key')
name_artist = []


# Spotify authorisation
def spotify_authorise():
    token_url = "https://accounts.spotify.com/api/token"
    token_params = {"grant_type": "client_credentials"}
    client_creds = f"{client_id}:{client_secret}"
    headers = {"Authorization": f"Basic {base64.b64encode(client_creds.encode()).decode()}"}
    res = requests.post(token_url, data=token_params, headers=headers)
    return res.json()


# get a list of strings consisting of the names of the track and the artist
def get_playlist_tracks(access_token, playlist_id):
    playlist_url = f"https://api.spotify.com/v1/playlists/{playlist_id}"
    headers = {"Authorization": f"Bearer {access_token}"}
    r = requests.get(playlist_url, headers=headers)
    tracks_items = r.json()["tracks"]["items"]
    for track in tracks_items:
        name = track["track"]["name"] + ","
        artists = ""
        for artist in track["track"]["artists"]:
            artists += str(artist["name"]) + ","
        name_artist.append(name + artists)


# get first video for each search query and compile into one anonymous youtube playlist
def get_youtube_playlist():
    tracks_and_names = []
    playlist_link = "http://www.youtube.com/watch_videos?video_ids="
    for name in name_artist:
        youtube = build("youtube", "v3", developerKey=yt_api_key)
        request = youtube.search().list(
            part="snippet",
            q=name,
            maxResults=1)
        response = request.execute()
        tracks_and_names.append(response['items'][0]["id"]["videoId"])
    playlist_link += ",".join(tracks_and_names)

    return playlist_link


def spotify_to_youtube(spotify_playlist_id):
    token = spotify_authorise()["access_token"]
    get_playlist_tracks(token, spotify_playlist_id)
    return get_youtube_playlist()
