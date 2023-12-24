import spotipy
from spotipy.oauth2 import SpotifyOAuth
import random
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import config
import numpy as np

class SpotifyPlaylistGenerator:
    def __init__(self, client_id, client_secret, redirect_uri):
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                                            client_secret=client_secret,
                                                            redirect_uri=redirect_uri,
                                                            scope='playlist-modify-public',
                                                            cache_path=".spotify_cache",
                                                            show_dialog=True,
                                                            open_browser=False))  # set show_dialog to False after the first run
        # Initialize class attributes to store selected values
        self.selected_danceability = None
        self.selected_energy = None
        self.selected_liveness = None
        self.selected_loudness = None

    def get_tracks_and_features(self, genre, num_tracks=100, danceability=None, energy=None, liveness=None, loudness=None):
        query = f'genre:{genre}'
        if danceability is not None:
            query += f' danceability:{danceability:.2f}'
        if energy is not None:
            query += f' energy:{energy:.2f}'
        if liveness is not None:
            query += f' liveness:{liveness:.2f}'
        if loudness is not None:
            query += f' loudness:-{abs(loudness)}'

        results = self.sp.search(q=query, type='track', limit=num_tracks)

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

    def create_histogram(self, data, title, xlabel, ylabel, filter_column, filtered_data=None):
        fig, ax = plt.subplots()

        # If filtered_data is provided, only use data within the subset
        if filtered_data is not None:
            filtered_indices = np.where(filtered_data)[0]
            data = data[filtered_indices]
            x_ticks = np.linspace(min(data), max(data), num=21)
        else:
            x_ticks = np.linspace(min(data), max(data), num=21)

        # Ensure data is not empty before proceeding
        if not data.any():
            print("No data available for the selected subset.")
            return None

        ax.hist(data, bins=20, color='skyblue', edgecolor='black')
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)

        # Set more refined ticks
        ax.set_xticks(x_ticks)
        ax.set_xticklabels([f'{tick:.2f}' for tick in x_ticks], rotation=45)

        # Initialize variables to store selection
        selected_x = None

        # Define the function to be called when a bar is clicked
        def onpick(event):
            nonlocal selected_x
            if isinstance(event.artist, Rectangle):
                selected_x = event.artist.get_x() + event.artist.get_width() / 2
                print(f'Selected x-value for {xlabel}: {selected_x}')

                # Update the selected value in the class attribute
                setattr(self, f'selected_{filter_column}', selected_x)

                # Close the plot after selection
                plt.close()

                # Call the next histogram
                next_column = self.get_next_filter_column(filter_column)
                next_data = getattr(self, f'{next_column}_values', None)
                next_filtered_data = getattr(self, f'selected_{filter_column}', None)
                if next_data is not None:
                    self.create_histogram(next_data, f'{next_column.capitalize()} Distribution for {genre}', next_column.capitalize(), 'Frequency', next_column, filtered_data=next_filtered_data)

        # Connect the pick event to the figure
        fig.canvas.mpl_connect('pick_event', onpick)

        # Add pickable rectangles for each bar
        for rect in ax.patches:
            rect.set_picker(True)

        # Show the plot
        plt.show()

        # Return the selected value
        return selected_x

    def get_next_filter_column(self, current_column):
        columns = ['danceability', 'energy', 'liveness', 'loudness']
        current_index = columns.index(current_column)
        return columns[current_index + 1] if current_index < len(columns) - 1 else None
        

    def generate_playlist(self, genre, playlist_name, num_tracks=20, **kwargs):
        danceability_min = kwargs.get('danceability_min', 0.5)
        energy_min = kwargs.get('energy_min', 0.5)
        liveness_min = kwargs.get('liveness_min', 0.5)
        loudness_max = kwargs.get('loudness_max', -10)

        query = f'genre:{genre} danceability:{danceability_min:.2f} energy:{energy_min:.2f} liveness:{liveness_min:.2f} loudness:-{abs(loudness_max)}'
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

if __name__ == "__main__":
    client_id = config.SPOTIPY_CLIENT_ID
    client_secret = config.SPOTIPY_CLIENT_SECRET
    redirect_uri = 'http://localhost:8888/callback'

    playlist_generator = SpotifyPlaylistGenerator(client_id, client_secret, redirect_uri)

    # Analyze genre and create histograms
    genre = input("Enter a genre for analysis: ")
    num_tracks = int(input("Enter the number of tracks to analyze: "))
    tracks, audio_features = playlist_generator.get_tracks_and_features(genre, num_tracks)

    danceability_values = np.array([feature['danceability'] for feature in audio_features])
    energy_values = np.array([feature['energy'] for feature in audio_features])
    liveness_values = np.array([feature['liveness'] for feature in audio_features])
    loudness_values = np.array([feature['loudness'] for feature in audio_features])

    # Call the create_histogram function
    selected_points_dance = playlist_generator.create_histogram(danceability_values, f'Danceability Distribution for {genre}', 'Danceability', 'Frequency', 'danceability')
    selected_points_energy = playlist_generator.create_histogram(energy_values, f'Energy Distribution for {genre}', 'Energy', 'Frequency', 'energy', filtered_data=selected_points_dance)
    selected_points_liveness = playlist_generator.create_histogram(liveness_values, f'Liveness Distribution for {genre}', 'Liveness', 'Frequency', 'liveness', filtered_data=selected_points_energy)
    selected_points_loudness = playlist_generator.create_histogram(loudness_values, f'Loudness Distribution for {genre}', 'Loudness', 'Frequency', 'loudness', filtered_data=selected_points_liveness)

    # Generate playlist
    genre = input("Enter a genre for the playlist: ")
    playlist_name = input("Enter a name for the playlist: ")
    num_tracks = int(input("Enter the number of tracks to include: "))

    # Since the selected points are lists, take the middle value for numeric parameters
    danceability_min = np.median(selected_points_dance) if selected_points_dance else 0.5
    energy_min = np.median(selected_points_energy) if selected_points_energy else 0.5
    liveness_min = np.median(selected_points_liveness) if selected_points_liveness else 0.5
    loudness_max = -np.sum(selected_points_loudness) / selected_points_loudness.size if selected_points_loudness else -10

    playlist_generator.generate_playlist(
        genre,
        playlist_name,
        num_tracks,
        danceability_min=danceability_min,
        energy_min=energy_min,
        liveness_min=liveness_min,
        loudness_max=loudness_max
    )