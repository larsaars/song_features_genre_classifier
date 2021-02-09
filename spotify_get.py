import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

search = input('Get data for search:')

with open('spotify_secrets.txt', 'r') as file:
    content = file.read().splitlines()
    client_id = content[0]
    client_secret = content[1]

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id,
                                                           client_secret=client_secret))

results = sp.search(q=search, limit=5)
tracks = []
for idx, track in enumerate(results['tracks']['items']):
    ft = sp.audio_features([track['id']])
    print(ft)
