import os
import sys
import time
import glob
import datetime
import sqlite3
import math
import numpy as np
from sklearn.cluster import KMeans
import hdf5_getters as GETTERS
import mysql.connector as mc
import pandas as pd
import fancyimpute
from sklearn.preprocessing import Imputer

file_path = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))
msd_path = os.path.join(file_path, 'msd')
msd_data_path = os.path.join(msd_path, 'data', 'A', 'A', 'A')
msd_addf_path = os.path.join(msd_path, 'AdditionalFiles')

song_infos = {}


def read_song_infos():
    print(msd_data_path)
    i = 1
    for root, dirs, files in os.walk(msd_data_path):
        files = glob.glob(os.path.join(root, '*'+'.h5'))
        for file in files:
            h5 = GETTERS.open_h5_file_read(file)
            id = GETTERS.get_song_id(h5).decode('UTF-8')
            song_infos[id] = {}
            song_infos[id]['title'] = GETTERS.get_title(h5).decode('UTF-8')
            song_infos[id]['artist'] = GETTERS.get_artist_name(
                h5).decode('UTF-8')
            if math.isnan(GETTERS.get_loudness(h5)):
                song_infos[id]['loudness'] = 0.0
            else:
                song_infos[id]['loudness'] = GETTERS.get_loudness(h5)
            if math.isnan(GETTERS.get_danceability(h5)):
                song_infos[id]['danceability'] = 0.0
            else:
                song_infos[id]['danceability'] = GETTERS.get_danceability(h5)
            if math.isnan(GETTERS.get_energy(h5)):
                song_infos[id]['energy'] = 0.0
            else:
                song_infos[id]['energy'] = GETTERS.get_energy(h5)
            if math.isnan(GETTERS.get_song_hotttnesss(h5)):
                song_infos[id]['hotttnesss'] = 0.0
            else:
                song_infos[id]['hotttnesss'] = GETTERS.get_song_hotttnesss(h5)
            if math.isnan(GETTERS.get_tempo(h5)):
                song_infos[id]['tempo'] = 0.0
            else:
                song_infos[id]['tempo'] = GETTERS.get_tempo(h5)
            h5.close()
            print('Song'+str(i)+' eingelesen')
            i += 1
    connection = mc.connect(host="sql7.freesqldatabase.com",
                            user="sql7236942",
                            passwd="ezVH8yrE2v",
                            db="sql7236942")
    cursor = connection.cursor()
    i = 1
    for key in song_infos:
        format_str = """INSERT INTO Songs (id, title, artist, danceability, energy, loudness, hotttnesss, tempo)
        VALUES ("{id}", "{title}", "{artist}", {danceability}, {energy}, {loudness}, {hotttnesss}, {tempo});"""

        sql_command = format_str.format(id=key, title=song_infos[key]['title'], artist=song_infos[key]['artist'], danceability=song_infos[key]['danceability'],
                                        energy=song_infos[key]['energy'], loudness=song_infos[key]['loudness'], hotttnesss=song_infos[key]['hotttnesss'], tempo=song_infos[key]['tempo'])
        cursor.execute(sql_command)
        print('Song'+str(i)+' in DB geschrieben')
    connection.commit()

    cursor.close()
    connection.close()
    print('fertig')
