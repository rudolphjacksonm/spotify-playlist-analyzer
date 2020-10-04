
# get all non-local tracks of a playlist
from spotipy.oauth2 import SpotifyClientCredentials
import json
import spotipy
import time
import sys

# playlist id of global top 50
PlaylistExample = '4As5Hiz998psWmWTRJmGpe'

# create spotipy client
client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
sp.trace = False

# load the first 100 songs
tracks = []
result = sp.playlist_items(PlaylistExample, additional_types=['track'])
tracks.extend(result['items'])

# if playlist is larger than 100 songs, continue loading it until end
while result['next']:
    result = sp.next(result)
    tracks.extend(result['items'])

# shows acoustic features for tracks for the given artist
tids = []
for t in tracks:
    print(t['track']['id'])
    tids.append(t['track']['id'])

start = time.time()
features = sp.audio_features(tids)
delta = time.time() - start
for feature in features:
    print(json.dumps(feature, indent=4))
    print()
    analysis = sp._get(feature['analysis_url'])
    #print(json.dumps(analysis, indent=4))
