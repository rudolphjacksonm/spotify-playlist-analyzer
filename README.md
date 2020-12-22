# Spotify Playlist Analyzer
Simple Python-based tool for displaying scatterplot data of audio features for all tracks from a given Spotify playlist ID.

### Usage
*NOTE: To work with the Spotify API, you'll have to register an application in the Spotify developer portal.* You can read more about the process [here](https://developer.spotify.com/documentation/web-api/quick-start/#set-up-your-account)

Provided you have registered an application with Spotify, the simplest way to prepare your environment is to set your Spotify client ID and secret as env vars. Spotipy, the Python library for interacting with the Spotify API, will look for the environment variables `SPOTIPY_CLIENT_ID` and `SPOTIPY_CLIENT_SECRET`.

To retrieve the playlist ID, right-click/cmd+click your playlist and select `Share > Copy Spotify URI` (see below). This will copy a link to your clipboard formatted as follows: spotify:playlist:<playlist_id>. Copy just the data after the last semicolon--this is your playlist ID.

![Alt text](docs/img/playlist_id.png?raw=true "Retrieving Playlist ID")

```bash
# Set env vars
export SPOTIPY_CLIENT_ID=<client_id>
export SPOTIPY_CLIENT_SECRET=<client_secret>

# Run the analyzer!
~/spotify-playlist-analyzer/> main.py --username my_username --playlist playlist_id
```

### Output
The analyzer combs through your playlist song by song and determines the audio features for each track. This is then graphed compared to the other songs using `matplotlib.pyplot`.

![Alt text](docs/img/valence.png?raw=true "Valence")
![Alt text](docs/img/energy.png?raw=true "Energy")
![Alt text](docs/img/danceability.png?raw=true "Danceability")
![Alt text](docs/img/tempo.png?raw=true "Tempo")