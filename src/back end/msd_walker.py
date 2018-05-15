import os
import glob
import math
import numpy as np
from sklearn.cluster import KMeans
import hdf5_getters as GETTERS
import mysql.connector as mc
import pyodbc
from os.path import dirname, abspath

file_path = dirname(dirname(dirname(abspath(__file__))))
msd_path = os.path.join(file_path, 'msd')
msd_data_path = os.path.join(msd_path, 'data')
msd_addf_path = os.path.join(msd_path, 'AdditionalFiles')

song_infos = {}

'''
def create_table():
    server = 'mrd.database.windows.net'
    database = 'mrd'
    username = 'qaywsx'
    password = 'w@970881'
    connection = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER=' +
                                server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD=' + password)
    cursor = connection.cursor()

    i = 1
    di = set()
    for root, dirs, files in os.walk(file_path):
        files = glob.glob(os.path.join(root, 'unique_artists.txt'))
        for file in files:
            f = open(file, "r", encoding="utf8")
            for line in f:
                l = line.split("<SEP>")
                if l[0] in di:
                    continue
                di.add(l[0])
                print(l[0]+'   '+l[3].replace("/n", ""))
                format_str = """INSERT INTO artistss (id, name) VALUES ('{id}', '{name}');"""
                sql_command = format_str.format(
                    id=l[0], name=l[3].replace("/n", ""))
                cursor.execute(sql_command)
                print('artist'+str(i)+'in DB geschrieben')
                i += 1

    connection.commit()
'''


def read_song_infos():
    i = 1
    for root, dirs, files in os.walk(msd_data_path):
        files = glob.glob(os.path.join(root, '*'+'.h5'))
        for file in files:
            h5 = GETTERS.open_h5_file_read(file)
            id = GETTERS.get_song_id(h5).decode('UTF-8')
            song_infos[id] = {}
            song_infos[id]['title'] = GETTERS.get_title(
                h5).decode('UTF-8').replace("'", "")
            song_infos[id]['artist'] = GETTERS.get_artist_name(
                h5).decode('UTF-8').replace("'", "")
            song_infos[id]['simartists'] = GETTERS.get_similar_artists(h5)
            song_infos[id]['timeSig'] = GETTERS.get_time_signature(h5)
            song_infos[id]['songkey'] = GETTERS.get_key(h5)
            song_infos[id]['mode'] = GETTERS.get_mode(h5)
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

    server = 'mrd.database.windows.net'
    database = 'mrd'
    username = 'qaywsx'
    password = 'w@970881'
    connection = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER=' +
                                server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD=' + password)
    cursor = connection.cursor()

    i = 1
    print('lösche alte Daten ...')
    cursor.execute("DELETE FROM songs;")
    print('Daten gelöscht')
    for key in song_infos:
        format_str = """INSERT INTO songs (id, title, artist, danceability, energy, loudness, hotttnesss, tempo, timeSig, songkey, mode)
        VALUES ('{id}', '{title}', '{artist}', {danceability}, {energy}, {loudness}, {hotttnesss}, {tempo}, {timeSig}, {songkey}, {mode});"""

        sql_command = format_str.format(id=key, title=song_infos[key]['title'], artist=song_infos[key]['artist'], danceability=song_infos[key]['danceability'], energy=song_infos[key]['energy'], loudness=song_infos[key]
                                        ['loudness'], hotttnesss=song_infos[key]['hotttnesss'], tempo=song_infos[key]['tempo'], timeSig=song_infos[key]['timeSig'], songkey=song_infos[key]['songkey'], mode=song_infos[key]['mode'])
        cursor.execute(sql_command)

        format_str2 = """INSERT INTO simartists (id, artist) VALUES ('{id}', '{artist}');"""
        '''
        for a in song_infos[key]['simartists']:
            a = a.decode('UTF-8')
            sql_command = format_str2.format(id=key, artist=a)
            cursor.execute(sql_command)
        '''
        print('Song'+str(i)+' in DB geschrieben')
        i += 1
    connection.commit()

    cursor.close()
    connection.close()
    print('fertig')
