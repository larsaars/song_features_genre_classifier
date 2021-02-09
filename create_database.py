"""
create database by collecting song features from playlists which we know the genre of
"""

import spotipy
import pandas as pd

# load credentials
with open('spotify_secrets.txt', 'r') as file:
    content = file.read().splitlines()
    client_id = content[0]
    client_secret = content[1]

# login
sp = spotipy.Spotify(auth_manager=spotipy.SpotifyClientCredentials(client_id=client_id,
                                                                   client_secret=client_secret))

genres = 'blues classical country disco hiphop jazz metal pop reggae rock electronic'.split()

playlists = '''7qACZGMjyo64TdUdKAegjp 3HYK6ri0GkvRcM6GkKh0hJ 
            4mijVkpSXJziPiOrK7YX4M 0ZVSWcJIf7cvycEn9HUvps 6MXkE0uYF4XwU4VTtyrpfP 
            5EyFMotmvSfDAZ4hSdKrbx 3pBfUFu8MkyiCYyZe849Ks 6gS3HhOiI17QNojjPuPzqc 
            0TcXdt4sbITbwCwwFbKYyd 7dowgSWOmvdpwNkGFMUs6e 6I0NsYzfoj7yHXyvkZYoRx'''.split()

columns = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness',
           'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'genre']

to_append = []

for g in zip(genres, playlists):

    # get playlist for given genre (default limit is 100)
    track_ids = sp.playlist_items(g[1],
                                  fields='items(track(id))')
    # some lists for gathering data
    tracks_list = []

    for track in track_ids['items']:
        tracks_list.append(track['track']['id'])

    # get audio features for 50 tracks at a time (spotipy only allows 50 at once)
    # code below can be looped if more tracks need to be analyzed
    tracks_af = sp.audio_features(tracks_list[:50])
    for track_num in range(0, 50):
        ft = tracks_af['track_num']
        track_data = [ft['danceability'], ft['energy'], ft['key'],
                      ft['loudness'], ft['mode'],
                      ft['speechiness'], ft['acousticness'],
                      ft['instrumentalness'], ft['liveness'],
                      ft['valence'], ft['tempo'], g[0]]
        to_append.append(track_data)

# create the data frame
audio_data = pd.DataFrame(to_append, columns=columns)

# and save as csv
audio_data.to_csv('datasets/songs_main_genres.csv', sep=';')
