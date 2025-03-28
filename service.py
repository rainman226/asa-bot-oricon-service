from bs4 import BeautifulSoup
import requests
from datetime import date, timedelta
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

#Oricon Settings
date = date.today() - timedelta(days = 1)
#p/1/
url = "https://www.oricon.co.jp/rank/js/d/" + date.strftime("%Y-%m-%d") + "/"

session = requests.Session()

#Spotify Setting
spotify_client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id="4e95af2ab9434bd385b856da4cdb88cd",
    client_secret=spotify_client_secret,
    redirect_uri="https://github.com/rainman226/asa-bot",
    scope="playlist-modify-public"
))
playlist_id = "4dQRIDb0a4JYRapKvJdT7c"

tracks_number = 0
tracks_added = 0

# Function to parse the Oricon page and extract track information
def parse_page(url):
    result = []

    response = session.get(url)
    if response.status_code != 200:
        return result
    
    soup = BeautifulSoup(response.content, "html.parser")

    # Find the section elements that contain the data
    for section in soup.select("section"):
        data = section.select_one(".inner")
        if not data:
            continue
        
        title = data.select_one("h2").get_text(strip=True)
        artist = data.select_one("p.name").get_text(strip=True)
        result.append(f"{artist} - {title}")
    return result

# Function to parse and entire day's worth of data
def parseDay():
    tracks = []
    for i in range(1, 4):
        tracks.extend(parse_page(url + "p/" + str(i) + "/"))
    
    return tracks

def search_track_on_spotify(artist, song_title):
    # Search for a track on Spotify, limiting the search to the Japan (JP) market.
    # Try searching by artist and song title in the Japan market
    query = f"artist:{artist} track:{song_title}"
    result = sp.search(q=query, type="track", limit=1)
    

    if result['tracks']['items']:
        return result['tracks']['items'][0]['id']  # Return the Spotify track ID
    
    # If not found, log that the track was not found
    print(f"Track not found on Spotify (Japan market): {artist} - {song_title}")
    return None 

def update_playlist(tracks):
    global tracks_added

    # Clear the playlist
    sp.playlist_replace_items(playlist_id, [])

    track_ids = []
    for track in tracks:
        # Split the artist and song title
        parts = track.split(" - ")
        if len(parts) == 2:
            artist = parts[0].strip()
            song_title = parts[1].strip()

            # Search for the track on Spotify
            track_id = search_track_on_spotify(artist, song_title)
            if track_id:
                track_ids.append(track_id)
                tracks_added += 1
    
    if track_ids:
        sp.playlist_add_items(playlist_id, track_ids)


oricon_tracks = parseDay()
update_playlist(oricon_tracks)
print(f"Added {tracks_added} tracks to the playlist.")
