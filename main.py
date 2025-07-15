from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json
import random

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")
    
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token


def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def fetch_artists_by_genre(token, genre_name, limit=20):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q=genre:{genre_name}&type=artist&limit={limit}"
    query_url = url + query
    
    result = get(query_url, headers=headers)
    artists = json.loads(result.content)["artists"]["items"]
    
    return artists

token = get_token()
user_genre_input = "melodic death metal"

formatted_genre = user_genre_input.strip().lower().replace(" ", "-")

artists = fetch_artists_by_genre(token, formatted_genre, limit=20)

if artists:
    chosen_artist = random.choice(artists)
    print(f"Randomly selected artist: {chosen_artist['name']}")
else:
    print("No artists found for that genre.")
