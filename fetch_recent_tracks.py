import os
import spotipy
import json
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth
from publish_to_pubsub import publish_tracks_to_pubsub
<<<<<<< HEAD
=======

load_dotenv()
>>>>>>> fix-local-changes


def fetch_recent_tracks(limit=10):
    """Fetches the 10 most recent tracks played by the user."""

    CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
    CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
    REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")

    SCOPE = "user-read-recently-played"

    sp_oauth = SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=SCOPE,
    )

    sp = spotipy.Spotify(auth_manager=sp_oauth)

    results = sp.current_user_recently_played(limit=10)

    # print(f"results: {json.dumps(results, indent=2)}")

    print("\n🎧 Your 10 Most Recent Tracks:")
    for idx, item in enumerate(results["items"]):
        track = item["track"]
        artists = ", ".join(artist["name"] for artist in track["artists"])
        print(
            f"{idx + 1}. {track['name']} by {artists} (Played at: {item['played_at']})"
        )
    return results["items"]


if __name__ == "__main__":
    tracks = fetch_recent_tracks()
    publish_tracks_to_pubsub(tracks)
