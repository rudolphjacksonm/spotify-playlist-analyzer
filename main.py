"""
Spotipy Playlist Analyzer -- Visualize the audio features of your Spotify playlist
"""
import argparse
import json
import pandas as pd
import matplotlib.pyplot as plt
import spotipy

from spotipy.oauth2 import SpotifyClientCredentials

client_credentials_manager = SpotifyClientCredentials()

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
    """Helper function for getting contents of a user playlist.
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

    with open('{}-{}.json'.format(username, playlist_id), 'w') as outfile:
        json.dump(songs, outfile)

    return get_playlist_enabled_songs(songs)

def get_playlist_audio_features(username, playlist_id, spotify_creds):
    """Returns audio features for all songs in a playlist
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
    #f, (ax1) = plt.subplots(1, 1, figsize=(3,3))
    #ax1.scatter(x='valence', y='name', data=df)
    #f, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4, figsize=(20,20))
    #ax1.scatter(x='uri', y='valence', data=df)
    #ax1.set_title('Valence')
    #ax2.scatter(x='uri', y='energy', data=df)
    #ax2.set_title('Energy')
    #ax3.scatter(x='tempo', y='danceability', data=df)
    #ax3.set_title('Tempo vs Danceability')
    #ax4.scatter(x='tempo', y='acousticness', data=df)
    #ax4.set_title('Tempo vs Acousticness')

    v = plt.figure(1)
    plt.scatter(x='valence', y='name', data=data_frame)
    plt.title('Playlist Valence')
    plt.xlabel('Valence', fontsize=10)
    plt.xlim([0,1])
    plt.ylabel('Track Name', fontsize=10)
    plt.tick_params(axis='both',labelsize=6)
    plt.show()
    e = plt.figure(2)
    plt.scatter(x='energy', y='name', data=data_frame)
    plt.title('Playlist Energy')
    plt.xlim([0,1])
    plt.xlabel('Energy', fontsize=10)
    plt.ylabel('Track Name', fontsize=10)
    plt.tick_params(axis='both',labelsize=6)
    plt.show()
    d = plt.figure(3)
    plt.scatter(x='danceability', y='name', data=data_frame)
    plt.title('Playlist Danceability')
    plt.xlim([0,1])
    plt.xlabel('Danceability', fontsize=10)
    plt.ylabel('Track Name', fontsize=10)
    plt.tick_params(axis='both',labelsize=6)
    plt.show()
    t = plt.figure(4)
    plt.scatter(x='tempo', y='name', data=data_frame)
    plt.title('Playlist Tempo')
    plt.xlim([0,250])
    plt.xlabel('Tempo', fontsize=10)
    plt.ylabel('Track Name', fontsize=10)
    plt.tick_params(axis='both',labelsize=6)
    plt.show()
    v.clf()
    e.clf()
    d.clf()
    t.clf()

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
