import os
import sys
import time
import glob
import datetime
import sqlite3
import numpy as np
from sklearn.cluster import KMeans
import hdf5_getters as GETTERS

msd_path = '/msd/MillionSongSubset'
msd_data_path = os.path.join(msd_path, 'data')
msd_addf_path = os.path.join(msd_path, 'AdditionalFiles')

song_infos = {}


def test():
    return 'Test'


def read_song_infos():
    for root, dirs, files in os.walk(msd_data_path):
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
