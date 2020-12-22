# Spotify Playlist Analyzer
## Displays audio features from a given Spotify playlist ID

### Usage
```python
~/spotify-playlist-analyzer/> main.py --username my_username --playlist playlist_id
```

### Output
The analyzer combs through your playlist song by song and determines the audio features for each track. This is then graphed compared to the other songs using `matplotlib.pyplot`.

![Alt text](docs/img/valence.png?raw=true "Valence")
![Alt text](docs/img/energy.png?raw=true "Energy")
![Alt text](docs/img/danceability.png?raw=true "Danceability")
![Alt text](docs/img/tempo.png?raw=true "Tempo")