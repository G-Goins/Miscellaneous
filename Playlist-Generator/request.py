import spotipy
from spotipy.oauth2 import SpotifyOAuth
import random
import matplotlib.pyplot as plt
import config

class SpotifyPlaylistGenerator:
    def __init__(self, client_id, client_secret, redirect_uri):
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                                            client_secret=client_secret,
                                                            redirect_uri=redirect_uri,
                                                            scope='playlist-modify-public'))

    def get_tracks_and_features(self, genre, num_tracks=50):
        results = self.sp.search(q=f'genre:{genre}', type='track', limit=num_tracks)

        # Check if the search was successful
        if not results or not results.get('tracks') or not results['tracks'].get('items'):
            print(f"No tracks found in the {genre} genre.")
            return [], []

        tracks = results['tracks']['items']
        track_ids = [track['id'] for track in tracks]
        
        # Check if any track IDs were found
        if not track_ids:
            print(f"No track IDs found for the {genre} genre.")
            return [], []

        audio_features = self.sp.audio_features(track_ids)
        
        return tracks, audio_features

    def create_histogram(self, data, title, xlabel, ylabel):
        plt.hist(data, bins=20, color='skyblue', edgecolor='black')
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.show()

    def generate_playlist(self, genre, playlist_name, num_tracks=20, danceability_min=0.5, energy_min=0.5, liveness_min=0.5, loudness_max=-10, tempo_range=(90, 120)):
        query = f'genre:{genre} danceability:{danceability_min:.2f} energy:{energy_min:.2f} liveness:{liveness_min:.2f} loudness:-{abs(loudness_max)} tempo:{tempo_range[0]}-{tempo_range[1]}'
        results = self.sp.search(q=query, type='track', limit=num_tracks)
        tracks = results['tracks']['items']

        if not tracks:
            print(f"No tracks found in the {genre} genre with the specified criteria.")
            return

        user_id = self.sp.me()['id']
        playlist = self.sp.user_playlist_create(user_id, playlist_name, public=True)

        random.shuffle(tracks)
        track_uris = [track['uri'] for track in tracks]
        self.sp.user_playlist_add_tracks(user_id, playlist['id'], track_uris)

        print(f'Playlist "{playlist_name}" created with {len(tracks)} tracks.')

    def genre_histogram_all_songs(self):
        results = self.sp.recommendations(seed_genres=[], limit=500)
        total_songs = results['tracks']['total']

        plt.bar(['All Genres'], [total_songs], color='skyblue')
        plt.title('Number of Songs Across All Genres')
        plt.xlabel('Genre')
        plt.ylabel('Number of Songs')
        plt.show()

if __name__ == "__main__":
    client_id = config.SPOTIPY_CLIENT_ID
    client_secret = config.SPOTIPY_CLIENT_SECRET
    redirect_uri = 'http://localhost:8888/callback'

    playlist_generator = SpotifyPlaylistGenerator(client_id, client_secret, redirect_uri)

    # Create a histogram for the number of songs per genre
    playlist_generator.genre_histogram_all_songs()

    # Analyze genre and create histograms
    genre = input("Enter a genre for analysis: ")
    num_tracks = int(input("Enter the number of tracks to analyze: "))
    tracks, audio_features = playlist_generator.get_tracks_and_features(genre, num_tracks)

    danceability_values = [feature['danceability'] for feature in audio_features]
    energy_values = [feature['energy'] for feature in audio_features]
    liveness_values = [feature['liveness'] for feature in audio_features]
    loudness_values = [feature['loudness'] for feature in audio_features]
    tempo_values = [feature['tempo'] for feature in audio_features]

    playlist_generator.create_histogram(danceability_values, f'Danceability Distribution for {genre}', 'Danceability', 'Frequency')
    playlist_generator.create_histogram(energy_values, f'Energy Distribution for {genre}', 'Energy', 'Frequency')
    playlist_generator.create_histogram(liveness_values, f'Liveness Distribution for {genre}', 'Liveness', 'Frequency')
    playlist_generator.create_histogram(loudness_values, f'Loudness Distribution for {genre}', 'Loudness', 'Frequency')
    playlist_generator.create_histogram(tempo_values, f'Tempo Distribution for {genre}', 'Tempo', 'Frequency')

    # Generate playlist
    genre = input("Enter a genre for the playlist: ")
    playlist_name = input("Enter a name for the playlist: ")
    num_tracks = int(input("Enter the number of tracks to include: "))
    danceability_min = float(input("Enter the minimum danceability (0.0 to 1.0): "))
    energy_min = float(input("Enter the minimum energy (0.0 to 1.0): "))
    liveness_min = float(input("Enter the minimum liveness (0.0 to 1.0): "))
    loudness_max = float(input("Enter the maximum loudness (e.g., -10): "))
    tempo_min = int(input("Enter the minimum tempo: "))
    tempo_max = int(input("Enter the maximum tempo: "))

    playlist_generator.generate_playlist(
        genre,
        playlist_name,
        num_tracks,
        danceability_min,
        energy_min,
        liveness_min,
        loudness_max,
        tempo_range=(tempo_min, tempo_max)
    )