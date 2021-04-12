import pandas as pd
from dataclasses import dataclass, field, asdict
from typing import List, Tuple
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import numpy as np
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json
import billboard
from collections import defaultdict, Counter
from models import *

# spotipy wraps the official spotify api providing simple python functions.
# TODO: Replace these two variables with the client_id and client_secret that you generated
CLIENT_ID = "926ee1ed38fe4f49acf4bb6dfe96fcc0"
CLIENT_SECRET = "8d5cdbe00e4f4a4a9d8f79dba990eba4"

# https://developer.spotify.com/dashboard/applications to get client_id and client_secret
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=CLIENT_ID,
                                                           client_secret=CLIENT_SECRET))


def getPlaylist(id: str) -> List[Track]:
    '''
    Given a playlist ID, returns a list of Track objects corresponding to the songs on the playlist. See
    models.py for the definition of dataclasses Track, Artist, and AudioFeatures.
    We need the audio features of each track to populate the audiofeatures list.
    We need the genre(s) of each artist in order to populate the artists in the artist list.

    We've written parts of this function, but it's up to you to complete it!
    '''

    # fetch tracks data from spotify given a playlist id
    playlistdata = sp.playlist(id)
    tracks = playlistdata['tracks']['items']

    # fetch audio features based on the data stored in the playlist result
    # TODO: build a list of track_ids from the tracks
    track_ids = []
    for i in tracks:
        track_ids.append(i['track']['id'])

    audio_features = sp.audio_features(track_ids)
    audio_info = {}  # Audio features list might not be in the same order as the track list
    for af in audio_features:
        audio_info[af['id']] = AudioFeatures(af['danceability'],
                                             af['energy'],
                                             af['key'],
                                             af['loudness'],
                                             af['mode'],
                                             af['speechiness'],
                                             af['acousticness'],
                                             af['instrumentalness'],
                                             af['liveness'],
                                             af['valence'],
                                             af['tempo'],
                                             af['duration_ms'],
                                             af['time_signature'],
                                             af['id'])

    # prepare artist dictionary
    # TODO: make a list of unique artist ids from tracks
    artist_ids = []
    for i in tracks:

        for j in i['track']['album']['artists']:
            artist_ids.append(j['id'])
    artists = {}

    for k in range(1 + len(artist_ids) // 50):  # can only request info on 50 artists at a time!
        artists_response = sp.artists(artist_ids[k * 50:min((k + 1) * 50, len(artist_ids))])  # what is this doing?
        for a in artists_response['artists']:
            # TODO: create the Artist for each id (see audio_info, above)
            artists[a['id']] = Artist(a['id'], a['name'], a['genres'])
    # populate track dataclass

    trackList = [Track(id=t['track']['id'],
                       # TODO: your code here    , \
                       name=t['track']['name'],
                       # TODO: your code here , \

                       artists=[artists[j['id']] for j in t['track']['album']['artists']],
                       # TODO: your code here ) \
                       audio_features=audio_info[t['track']['id']])
                 for t in tracks]
    return trackList


''' this function is just a way of naming the list we're using. You can write
additional functions like "top Canadian hits!" if you want.'''


def getHot100() -> List[Track]:
    # Billboard hot 100 Playlist ID URI
    hot_100_id = "6UeSakyzhiEt4NB3UAd6NQ"
    return getPlaylist(hot_100_id)


# ---------------------------------------------------------------------

# part1: implement helper functions to organize data into DataFrames

def getGenres(t: Track) -> List[str]:
    '''
    TODO
    Takes in a Track and produce a list of unique genres that the artists of this track belong to
    '''
    temp = []
    for i in t.artists:
        temp.append(i.genres)
    final = []
    for i in temp:
        for j in temp:
            if type(j) == list:
                for n in j:
                    if n not in final:
                        final.append(n)
            elif j not in final:
                final.append(i)
    return final


def doesGenreContains(t: Track, genre: str) -> bool:
    '''
    TODO
    Checks if the genres of a track contains the key string specified
    For example, if a Track's unique genres are ['pop', 'country pop', 'dance pop']
    doesGenreContains(t, 'dance') == True
    doesGenreContains(t, 'pop') == True
    doesGenreContains(t, 'hip hop') == False
    '''
    check = False
    for i in t.artists:
        if genre in i.genres:
            check = True
            break
    return check


def getTrackDataFrame(tracks: List[Track]) -> pd.DataFrame:
    '''
    This function is given.
    Prepare dataframe for a list of tracks
    audio-features: 'danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness',
                    'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo',
                    'duration_ms', 'time_signature', 'id',
    track & artist: 'track_name', 'artist_ids', 'artist_names', 'genres',
                    'is_pop', 'is_rap', 'is_dance', 'is_country'
    '''
    # populate records
    records = []
    for t in tracks:
        to_add = asdict(t.audio_features)  # converts the audio_features object to a dict
        to_add["track_name"] = t.name
        to_add["artist_ids"] = list(map(lambda a: a.id, t.artists))  # we will discuss this in class
        to_add["artist_names"] = list(map(lambda a: a.name, t.artists))
        to_add["genres"] = getGenres(t)
        to_add["is_pop"] = doesGenreContains(t, "pop")
        to_add["is_rap"] = doesGenreContains(t, "rap")
        to_add["is_dance"] = doesGenreContains(t, "dance")
        to_add["is_country"] = doesGenreContains(t, "country")

        records.append(to_add)

    # create dataframe from records
    df = pd.DataFrame.from_records(records)
    return df


# minor testing code:
top100Tracks = getHot100()
df = getTrackDataFrame(top100Tracks)


# you may want to experiment with the dataframe now!

# ---------------------------------------------------------------------
# Part2: The most popular artist of the week

def artist_with_most_tracks(tracks: List[Track]) -> (Artist, int):
    '''
    TODO
    List of tracks -> (artist, number of tracks the artist has)
    This function finds the artist with most number of tracks on the list
    If there is a tie, you may return any of the artists
    '''
    a = []
    temp = {}
    for i in tracks:
        for j in i.artists:
            a.append(j.id)
            temp[j.id] = {'id': j.id, 'name': j.name, 'genres': j.genres}

    tally = Counter(a)  # these structures will be useful!
    a = max(tally, key=tally.get)

    return Artist(id=temp[a]['id'], name=temp[a]['name'], genres=temp[a]['genres']), tally[a]


# minor testing code:
artist, num_track = artist_with_most_tracks(top100Tracks)
print("%s has the most number of tracks on this week's Hot 100 at a whopping %d tracks!" % (artist.name, num_track))

"""2.2"""
# Do you think this is a good measurement for popularity? Come up with an alternative definition in your writeup
# and justify in the write-up! (You don't need to code it out)
"""I do not think that the number of songs on the top 100 is a good measure of popularity for artists, an alternative 
methode could be to measure popularity by how many individual listeners an artist has """

# Part3: Data Visualization

# 3.1 scatter plot of dancability-tempo colored by genre is_rap
plt.style.use('dark_background')

data_rap = df[df['is_rap'] == True]
data = df[df['is_rap'] == False]



plt.scatter(data_rap['danceability'], data_rap['speechiness'], marker='.', color='coral', label="Rap Songs")

plt.scatter(data['danceability'], data['speechiness'], marker='.', color='teal', label="Non Rap Songs")
plt.xlabel('Danceability')
plt.ylabel('Speechiness')
plt.title('Danceability/Speechiness Scatter Plot')
plt.legend()
plt.show()

# 3.2 scatter plot (ask your own question)


# Describe in one sentence what the plot shows about the rap genre.
"""That those songs are above the mean of danceability and speechiness scores compareed to other top 100 songs"""


# This is Spotify's take on danceability and speechiness. Do you think it is reasonable based on the result of the plot?
"""Yes, my opinion agrees with the values form the Spotify API"""



"""3.2 Ask your own question"""




# Come up with a question that explores the relationship between audio features and genre/artist. Answer and justify
# your question in the write up. Include at least one scatter plot in your answer. A few ideas to start off with:

"""is there any significant diference in the averages for each audio feataure between genres and how do they differ from each other?"""

pop_data = df[df['is_pop']]
rap_data = df[df['is_rap']]
dance_data = df[df['is_dance']]
country_data = df[df['is_country']]



data = [pop_data, rap_data, dance_data, country_data]



xaxis = ['danceability_mean', 'energy_mean','speechiness_mean','acousticness_mean']
j = 1
colour = ['teal', 'coral', 'turquoise', 'wheat', 'skyblue','palegreen','palevioletred','deeppink','orchid','violet','royalblue','aqua','ivory','lavander','crimson' ]
legends = ['is_pop','is_rap','is_dance','is_country']
x = np.arange(len(xaxis))

fig, ax = plt.subplots()
dict = {}
n= 0
for i in data:
    yaxis = []
    yaxis.append(np.mean(i['danceability']))
    yaxis.append(np.mean(i['energy']))
    yaxis.append(np.mean(i['speechiness']))
    yaxis.append(np.mean(i['acousticness']))

    dict[legends[j]] = ax.bar(x - (n*j*.25)/2, yaxis, color=colour[n], width=0.25,label = legends[n])



    n +=1
    j *= -1


ax.set_xticklabels(xaxis)
ax.set_ylabel('Scores')
ax.legend()
plt.show()
xaxis = ['energy','speechiness','acousticness']
ylabel = ['pop','rap','dance','country']
n = 0
m = 0
for i in data:
    yaxis = []
    yaxis.append((i['energy']))
    yaxis.append((i['speechiness']))
    yaxis.append((i['acousticness']))
    for j in range(len(yaxis)-1):
        plt.scatter(i['danceability'], yaxis[j], marker='.', color=colour[n], label=( ylabel[n] +" " + xaxis[j]))
        m+=1
    n+=1
plt.xlabel("Danceability")
plt.ylabel("non unit values")
plt.title("'energy','speechiness','acousticness' vs  'danceability'")
plt.legend()
plt.show()

"""In general the mean values for 'danceability_mean', 'energy_mean','speechiness_mean','acousticness_mean' are not 
very far from each sorting by genres, but in the speechiness_mean rap music takes a very significant lead(%wise) 
compared to the other genres (dance has currently no song on the top 100) """
# What are the distinct audio features that separate country music from the rest of the tracks on the Hot 100 list?

"""I found out that has a very significantly lower speechiness_mean than other genres (except dance that currently 
holds 0 spots in th top 100) (x labels are wrong couldnt figure out how to align the labels to the bars)"""


# Are there genres that do not overlap with each other at all in some feature space? Feel free to modify



# getTrackDataFrame(tracks: List[Track]) -> pd.DataFrame to include attributes that you think will be useful. If you
# want to query a playlist different from Billboard Hot 100, call getPlaylist(id: str) -> List[Track] with a playlist
# id of your choosing. You can find playlist id of a playlist here.


# (Bonus) Part4:
# take a song that's not on the list, compute distance with the songs on the list and see if we get the same artist
