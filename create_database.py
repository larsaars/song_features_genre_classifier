"""
create database by collecting song features from playlists which we know the genre of
"""

import spotipy
import pandas as pd
import global_variables as gv

# load credentials
with open('spotify_secrets.txt', 'r') as file:
    content = file.read().splitlines()
    client_id = content[0]
    client_secret = content[1]

# login
sp = spotipy.Spotify(auth_manager=spotipy.SpotifyClientCredentials(client_id=client_id,
                                                                   client_secret=client_secret))

to_append = []

for g in zip(gv.genres, gv.playlists):

    # print progress
    print(g[0])

    # get playlist for given genre (default limit is 100)
    track_ids = sp.playlist_items(g[1],
                                  fields='items(track(id))', limit=100)
    # some lists for gathering data
    tracks_list = []

    for track in track_ids['items']:
        tracks_list.append(track['track']['id'])

    # get audio features for 50 tracks at a time (spotipy only allows 50 at once)
    # code below can be looped if more tracks need to be analyzed
    for from_idx in range(0, len(tracks_list), 50):

        to_idx = from_idx + 50
        if to_idx > len(tracks_list):
            to_idx = len(tracks_list)

        tracks_af = sp.audio_features(tracks_list[from_idx:to_idx])

        for track_num in range(0, 50):
            ft = tracks_af[track_num]
            track_data = [g[0], ft['danceability'], ft['energy'], ft['key'],
                          ft['loudness'], ft['mode'],
                          ft['speechiness'], ft['acousticness'],
                          ft['instrumentalness'], ft['liveness'],
                          ft['valence'], ft['tempo']]
            to_append.append(track_data)

# create the data frame
audio_data = pd.DataFrame(to_append, columns=gv.columns)

# and save as csv
audio_data.to_csv('datasets/songs_main_genres.csv', sep=';', index=False)
