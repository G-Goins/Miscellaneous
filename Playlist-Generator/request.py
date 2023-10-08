# Load in packages
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import random
import config

#Access variables
client_id = config.SPOTIPY_CLIENT_ID
client_secret = config.SPOTIPY_CLIENT_SECRET
redirect_uri = 'http://localhost:8888/callback'

# Spotify API authentication
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri,
                                               scope='playlist-modify-public'))

# Function to generate a playlist based on a genre
def generate_playlist(genre, playlist_name, num_tracks=20):
    # Search for tracks in the specified genre
    results = sp.search(q=f'genre:{genre}', type='track', limit=num_tracks)
    tracks = results['tracks']['items']

    if not tracks:
        print(f"No tracks found in the {genre} genre.")
        return

    # Create a new playlist
    user_id = sp.me()['id']
    playlist = sp.user_playlist_create(user_id, playlist_name, public=True)

    # Shuffle the tracks
    random.shuffle(tracks)

    # Add tracks to the playlist
    track_uris = [track['uri'] for track in tracks]
    sp.user_playlist_add_tracks(user_id, playlist['id'], track_uris)

    print(f'Playlist "{playlist_name}" created with {len(tracks)} tracks.')

if __name__ == "__main__":
    genre = input("Enter a genre for the playlist: ")
    playlist_name = input("Enter a name for the playlist: ")
    num_tracks = int(input("Enter the number of tracks to include: "))

    generate_playlist(genre, playlist_name, num_tracks)
          


