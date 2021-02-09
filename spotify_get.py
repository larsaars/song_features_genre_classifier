import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pickle as pkl
from sklearn.neighbors import KNeighborsClassifier

# load credentials
with open('spotify_secrets.txt', 'r') as file:
    content = file.read().splitlines()
    client_id = content[0]
    client_secret = content[1]

# login
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id,
                                                           client_secret=client_secret))

# load model
print('<< loading model...')
model: KNeighborsClassifier
with open('models/model.pkl', 'rb') as file:
    model = pkl.load(file)

# print when done loading
print('<< Done! Enter a song name:')

# loop prediction for input
while True:
    inp = input('>> ')

    # break if input is 'q'
    if inp == 'q':
        break

    # get first result
    song_results = sp.search(q=inp, limit=1)

    # call in loop for auto skipping if no results
    for idx, track in enumerate(song_results['tracks']['items']):
        # print the name and artist of track
        artists = []
        for idx2, artist in enumerate(track['artists']):
            artists.append(artist['name'])

        print('<< %s - %s' % (track['name'], artists[0] if len(artists) == 1 else str(artists)))
        # else predict from features
        # get the features
        ft = sp.audio_features(track['id'])
        # extract to list to be predictable
        print(ft)
