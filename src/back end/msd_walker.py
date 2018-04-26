import os
import sys
import time
import glob
import datetime
import sqlite3
import numpy as np
from sklearn.cluster import KMeans
import hdf5_getters as GETTERS

msd_subset_path = 'C:/Users/jzenk/OneDrive/Dokumente/Uni HH BA SSE/S04 SS18 Projekt Wirtschaftsinformatik/MillionSongSubset'
msd_subset_data_path = os.path.join(msd_subset_path, 'data')
msd_subset_addf_path = os.path.join(msd_subset_path, 'AdditionalFiles')

song_infos = {}


def test():
    f = GETTERS.open_h5_file_read(
        'C:/Users/jzenk/Documents/GitHub/music-recommender/src/back end/TRAAAAW128F429D538.h5')
    X = np.array([[1, 2], [1, 4], [1, 0], [4, 2], [4, 4], [4, 0]])
    kmeans = KMeans(n_clusters=2, random_state=0).fit(X)
    print(kmeans.labels_)
    print(kmeans.predict([[0, 0], [4, 4]]))
    print(kmeans.cluster_centers_)
    print(GETTERS.get_tempo(f))
    print(GETTERS.get_danceability(f))
    print(GETTERS.get_loudness(f))
    return GETTERS.get_artist_name(f)


def read_song_infos():
    for root, dirs, files in os.walk(msd_subset_data_path):
        files = glob.glob(os.path.join(root, '*'+'.h5'))
        for file in files:
            h5 = GETTERS.open_h5_file_read(file)
            id = GETTERS.get_song_id(h5)
            song_infos[id] = {}
            song_infos[id]['Artist'] = GETTERS.get_artist_name(h5)
            song_infos[id]['loudness'] = GETTERS.get_loudness(h5)
            song_infos[id]['danceability'] = GETTERS.get_danceability(h5)
            song_infos[id]['energy'] = GETTERS.get_energy(h5)
            song_infos[id]['hotttnesss'] = GETTERS.get_song_hotttnesss(h5)
            song_infos[id]['tempo'] = GETTERS.get_tempo(h5)
            h5.close()
    print(song_infos)
    print(song_infos[b'SOFAOMI12A6D4FA2D8']['energy'] is not 0.0)
    print(song_infos[b'SOLHMRA12A8C13234A']['hotttnesss'] is not 0.0)
