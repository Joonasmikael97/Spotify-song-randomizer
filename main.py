from flask import Flask, request, jsonify,send_from_directory
from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json
import random

load_dotenv()

app = Flask(__name__)

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

@app.route('/random-artist')
def random_artist():
    genre = request.args.get('genre', default="", type=str).strip().lower().replace(" ", "-")
    if not genre:
        return jsonify({"error": "Genre parameter is required"}), 400
    
    try:
        token = get_token()
        artists = fetch_artists_by_genre(token, genre, limit=20)
        if not artists:
            return jsonify({"error": f"No artists found for genre '{genre}'"}), 404

        chosen_artist = random.choice(artists)
        return jsonify({
            "name": chosen_artist['name'],
            "id": chosen_artist['id'],
            "genres": chosen_artist['genres'],
            "followers": chosen_artist['followers']['total'],
            "spotify_url": chosen_artist['external_urls']['spotify']
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
   
@app.route("/")
def index():
    return send_from_directory('.', 'index.html')


if __name__ == '__main__':
    app.run(debug=True)
