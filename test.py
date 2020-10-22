import argparse
import pprint
import sys
import os
import subprocess
import json
import spotipy
import spotipy.util as util
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from spotipy.oauth2 import SpotifyClientCredentials


client_credentials_manager = SpotifyClientCredentials()


def get_playlist_content(username, playlist_id, sp):
    offset = 0
    songs = []
    while True:
        content = sp.user_playlist_tracks(username, playlist_id, fields=None,
                                          limit=100, offset=offset, market=None)
        songs += content['items']
        if content['next'] is not None:
            offset += 100
        else:
            break

    with open('{}-{}'.format(username, playlist_id), 'w') as outfile:
        json.dump(songs, outfile)


def get_playlist_audio_features(username, playlist_id, sp):
    offset = 0
    songs = []
    items = []
    ids = []
    # duplicated code here, could probably strip out?
    while True:
        content = sp.user_playlist_tracks('chrisredfield306', '4As5Hiz998psWmWTRJmGpe', fields=None, limit=100, offset=offset, market=None)
        songs += content['items']
        if content['next'] is not None:
            offset += 100
        else:
            break

    for i in songs:
        ids.append(i['track']['id'])

    index = 0
    audio_features = []
    while index < len(ids):
        audio_features += sp.audio_features(ids[index:index + 50])
        index += 50

    features_list = []
    for features in audio_features:
        features_list.append([features['energy'], features['liveness'],
                                features['tempo'], features['speechiness'],
                                features['acousticness'], features['instrumentalness'],
                                features['time_signature'], features['danceability'],
                                features['key'], features['duration_ms'],
                                features['loudness'], features['valence'],
                                features['mode'], features['type'],
                                features['uri']])
    # Spit out feature list to json for local testing
    with open('{}-{}'.format(username, f'{playlist_id}_features'), 'w') as outfile:
        json.dump(features_list, outfile)

    df = pd.DataFrame(features_list, columns=['energy', 'liveness',
                                                'tempo', 'speechiness',
                                                'acousticness', 'instrumentalness',
                                                'time_signature', 'danceability',
                                                'key', 'duration_ms', 'loudness',
                                                'valence', 'mode', 'type', 'uri'])

    df.to_csv('{}-{}.csv'.format(username, playlist_id), index=False)

    # Display plot
    f, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4, ffigsize=(10,10))
    ax1.scatter(x='tempo', y='valence', data=df)
    ax1.set_title('Tempo vs Valence')
    ax2.scatter(x='tempo', y='energy', data=df)
    ax2.set_title('Tempo vs Energy')
    ax3.scatter(x='tempo', y='danceability', data=df)
    ax3.set_title('Tempo vs Danceability')
    ax4.scatter(x='tempo', y='acousticness', data=df)
    ax4.set_title('Tempo vs Acousticness')
    plt.show()

def get_user_playlist(username, sp):
    playlists = sp.user_playlists(username)
    for playlist in playlists['items']:
        print(("Name: {}, Number of songs: {}, Playlist ID: {} ".
              format(playlist['name'].encode('utf8'),
                     playlist['tracks']['total'],
                     playlist['id'])))


def main(username, playlist):
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    print("Getting user playlist")
    get_user_playlist(username, sp)
    print("Getting playlist content")
    get_playlist_content(username, playlist, sp)
    print("Getting playlist audio features")
    get_playlist_audio_features(username, playlist, sp)


if __name__ == '__main__':
    print('Starting...')
    parser = argparse.ArgumentParser(description='description')
    parser.add_argument('--username', help='username')
    parser.add_argument('--playlist', help='username')
    args = parser.parse_args()
    main(args.username, args.playlist)
