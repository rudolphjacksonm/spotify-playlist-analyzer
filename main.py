"""
Spotipy Playlist Analyzer -- Visualize the audio features of your Spotify playlist
"""
import argparse
import json
import pandas as pd
import matplotlib
# Make sure that we are using QT5
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
from PyQt5 import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import spotipy

from spotipy.oauth2 import SpotifyClientCredentials

client_credentials_manager = SpotifyClientCredentials()

font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 8}

matplotlib.rc('font', **font)

class ScrollableWindow(QtWidgets.QMainWindow):
    def __init__(self, fig):
        self.qapp = QtWidgets.QApplication([])

        QtWidgets.QMainWindow.__init__(self)
        self.widget = QtWidgets.QWidget()
        self.setCentralWidget(self.widget)
        self.widget.setLayout(QtWidgets.QVBoxLayout())
        self.widget.layout().setContentsMargins(0,0,0,0)
        self.widget.layout().setSpacing(0)

        self.fig = fig
        self.canvas = FigureCanvas(self.fig)
        self.canvas.draw()
        self.scroll = QtWidgets.QScrollArea(self.widget)
        self.scroll.setWidget(self.canvas)

        self.nav = NavigationToolbar(self.canvas, self.widget)
        self.widget.layout().addWidget(self.nav)
        self.widget.layout().addWidget(self.scroll)

        self.show()
        exit(self.qapp.exec_()) 

def get_playlist_enabled_songs(songs):
    """
    Helper function for determining which songs in a playlist
    are shown as enabled in the target market.
    """
    enabled_songs = []
    for i in songs:
        if i['track']['is_playable'] is True:
            enabled_songs.append(i)
            print("Enabled track {}" .format(i['track']['name']))
        else:
            print("Skipping track {} as it is disabled." .format(i['track']['name']))

    return enabled_songs

def get_playlist_content(username, playlist_id, spotify_creds):
    """
    Helper function for getting contents of a user playlist.
    """
    offset = 0
    songs = []
    while True:
        content = spotify_creds.user_playlist_tracks(username, playlist_id, fields=None,
                                          limit=100, offset=offset, market='gb')
        songs += content['items']
        if content['next'] is not None:
            offset += 100
        else:
            break

    return get_playlist_enabled_songs(songs)

def get_playlist_audio_features(username, playlist_id, spotify_creds):
    """
    Returns audio features for all songs in a playlist
    """
    ids = []

    songs = get_playlist_content(username, playlist_id, spotify_creds)
    for i in songs:
        ids.append(i['track']['id'])

    index = 0
    audio_features = []
    while index < len(ids):
        audio_features += spotify_creds.audio_features(ids[index:index + 50])
        index += 50

        features_list = []
        fidx = 0
        for features in audio_features:
            features_list.append([features['energy'], features['liveness'],
                                    features['tempo'], features['speechiness'],
                                    features['acousticness'], features['instrumentalness'],
                                    features['time_signature'], features['danceability'],
                                    features['key'], features['duration_ms'],
                                    features['loudness'], features['valence'],
                                    features['mode'], features['type'],
                                    features['uri'], songs[fidx]['track']['name']])
            fidx += 1

        return features_list

def get_playlist_dataframe(data):
    """Takes raw playlist data, converts to DataFrame, and displays plots
    """
    data_frame = pd.DataFrame(data, columns=['energy', 'liveness',
                                                'tempo', 'speechiness',
                                                'acousticness', 'instrumentalness',
                                                'time_signature', 'danceability',
                                                'key', 'duration_ms', 'loudness',
                                                'valence', 'mode', 'type', 'uri', 'name'])

    data_frame.to_csv('{}.csv'.format("playlist_id"), index=False)
    
    # Display plots as subplots
    features = [
        'valence',
        'energy',
        'tempo',
        'danceability'
    ]
    fig, axs = plt.subplots(len(features), figsize=(5,15))
    for f in range(len(features)):
        axs[f].scatter(x=features[f], y='name', data=data_frame)
        axs[f].set_title(features[f])
        axs[f].set_yticks([])
    
    a = ScrollableWindow(fig)

def main(username, playlist_id):
    """
        Main function
    """
    spotify_creds = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    print("Getting playlist audio features")
    data = get_playlist_audio_features(username, playlist_id, spotify_creds)
    get_playlist_dataframe(data)


if __name__ == '__main__':
    print('Starting...')
    parser = argparse.ArgumentParser(description='description')
    parser.add_argument('--username', help='username')
    parser.add_argument('--playlist-id', help='username')
    args = parser.parse_args()
    main(args.username, args.playlist_id)
