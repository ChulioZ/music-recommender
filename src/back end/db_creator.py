import os
import time
import datetime
import glob
import math
import numpy as np
import hdf5_getters as GETTERS
import mysql.connector as mc
import pyodbc
from os.path import dirname, abspath
from mice import MICE

file_path = dirname(dirname(dirname(abspath(__file__))))
msd_path = os.path.join(file_path, 'msd')
msd_data_path = os.path.join(msd_path, 'data')
msd_addf_path = os.path.join(msd_path, 'AdditionalFiles')


def change_db():
    # connect to the data base
    server = 'mrd.database.windows.net'
    database = 'mrd'
    username = 'qaywsx'
    password = 'w@970881'
    connection = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER=' +
                                server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD=' + password)
    cursor = connection.cursor()

    # replace with the SQL command you want to execute
    #cursor.execute("ALTER TABLE songs ADD label int;")
    connection.commit()
    cursor.close()
    connection.close()


def build_db():
    start = time.time()

    # read all relevant infos from the songs and store them in a dictionary
    song_infos = {}
    i = 0
    ids = set()
    missing_hotttnesss_values = 0
    missing_timeSig_values = 0
    missing_songkey_values = 0
    missing_mode_values = 0
    missing_loudness_values = 0
    missing_tempo_values = 0
    for root, dirs, files in os.walk(msd_data_path):
        files = glob.glob(os.path.join(root, '*'+'.h5'))
        for file in files:
            h5 = GETTERS.open_h5_file_read(file)
            id = GETTERS.get_song_id(h5).decode('UTF-8')
            if id not in ids:
                i += 1
                ids.add(id)
                song_infos[i] = {}
                song_infos[i]['id'] = id
                song_infos[i]['title'] = GETTERS.get_title(
                    h5).decode('UTF-8').replace("'", "")
                song_infos[i]['artist'] = GETTERS.get_artist_name(
                    h5).decode('UTF-8').replace("'", "")
                song_infos[i]['simartists'] = GETTERS.get_similar_artists(h5)
                if math.isnan(GETTERS.get_time_signature(h5)):
                    song_infos[i]['timeSig'] = np.NaN
                    missing_timeSig_values += 1
                else:
                    song_infos[i]['timeSig'] = GETTERS.get_time_signature(h5)
                if math.isnan(GETTERS.get_key(h5)):
                    song_infos[i]['songkey'] = np.NaN
                    missing_songkey_values += 1
                else:
                    song_infos[i]['songkey'] = GETTERS.get_key(h5)
                if math.isnan(GETTERS.get_mode(h5)):
                    song_infos[i]['mode'] = np.NaN
                    missing_mode_values += 1
                else:
                    song_infos[i]['mode'] = GETTERS.get_mode(h5)
                if math.isnan(GETTERS.get_loudness(h5)):
                    song_infos[i]['loudness'] = np.NaN
                    missing_loudness_values += 1
                else:
                    song_infos[i]['loudness'] = GETTERS.get_loudness(h5)
                if math.isnan(GETTERS.get_tempo(h5)):
                    song_infos[i]['tempo'] = np.NaN
                    missing_tempo_values += 1
                else:
                    song_infos[i]['tempo'] = GETTERS.get_tempo(h5)
                if math.isnan(GETTERS.get_song_hotttnesss(h5)):
                    song_infos[i]['hotttnesss'] = np.NaN
                    missing_hotttnesss_values += 1
                else:
                    song_infos[i]['hotttnesss'] = GETTERS.get_song_hotttnesss(
                        h5)
                h5.close()
                print('Song'+str(i)+' eingelesen')
            else:
                print('Song-ID doppelt')

    # normalize the values
    for key in ['loudness', 'hotttnesss', 'tempo', 'timeSig', 'songkey', 'mode']:
        max_value = -float("inf")
        min_value = float("inf")
        for index in song_infos:
            max_value = max(max_value, float(song_infos[index][key]))
            min_value = min(min_value, float(song_infos[index][key]))
        for index in song_infos:
            song_infos[index][key] = (
                float(song_infos[index][key]) - min_value)/(max_value - min_value) * 100
            print('Song'+str(index)+'normalisiert')

    # impute missing values via fancyimpute MICE imputation and store the new values in the dictionary
    song_array = np.array([[song_infos[1]['timeSig'], song_infos[1]['songkey'], song_infos[1]
                            ['mode'], song_infos[1]['loudness'], song_infos[1]['tempo'], song_infos[1]['hotttnesss']]])
    for index in range(2, i+1):
        newar = np.array([[song_infos[index]['timeSig'], song_infos[index]['songkey'], song_infos[index]['mode'],
                           song_infos[index]['loudness'], song_infos[index]['tempo'], song_infos[index]['hotttnesss']]])
        song_array = np.concatenate((song_array, newar))
        print('song'+str(index)+'konkateniert')
    mc = MICE()
    a = mc.complete(song_array)
    for song in range(1, i+1):
        song_infos[song]['timeSig'] = a[song-1, 0]
        song_infos[song]['songkey'] = a[song-1, 1]
        song_infos[song]['mode'] = a[song-1, 2]
        song_infos[song]['loudness'] = a[song-1, 3]
        song_infos[song]['tempo'] = a[song-1, 4]
        song_infos[song]['hotttnesss'] = a[song-1, 5]
        print('songinfos'+str(song)+'aktualisiert')

    # connect to the data base
    server = 'mrd.database.windows.net'
    database = 'mrd'
    username = 'qaywsx'
    password = 'w@970881'
    connection = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER=' +
                                server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD=' + password)
    cursor = connection.cursor()

    # delete old data in the data base
    print('lösche alte Daten ...')
    cursor.execute("DELETE FROM songs;")
    print('Daten gelöscht')

    # save each song in the data base
    for key in song_infos:
        format_str = """INSERT INTO songs (id, title, artist, loudness, hotttnesss, tempo, timeSig, songkey, mode)
        VALUES ('{id}', '{title}', '{artist}', {loudness}, {hotttnesss}, {tempo}, {timeSig}, {songkey}, {mode});"""

        sql_command = format_str.format(id=song_infos[key]['id'], title=song_infos[key]['title'], artist=song_infos[key]['artist'], loudness=song_infos[key]['loudness'], hotttnesss=song_infos[key]
                                        ['hotttnesss'], tempo=song_infos[key]['tempo'], timeSig=song_infos[key]['timeSig'], songkey=song_infos[key]['songkey'], mode=song_infos[key]['mode'])
        cursor.execute(sql_command)
        print('Song'+str(key)+' in DB geschrieben')
    connection.commit()

    cursor.close()
    connection.close()
    print('fertig')
    print(str(missing_hotttnesss_values)+'missing hotttnesss values')
    print(str(missing_loudness_values)+'missing loudness values')
    print(str(missing_mode_values)+'missing mode values')
    print(str(missing_songkey_values)+'missing songkey values')
    print(str(missing_tempo_values)+'missing tempo values')
    print(str(missing_timeSig_values)+'missing timeSig values')

    end = time.time()
    print(str(datetime.timedelta(seconds=end-start)))


def add_labels_to_db(labels, ids):
    # connect to the data base
    server = 'mrd.database.windows.net'
    database = 'mrd'
    username = 'qaywsx'
    password = 'w@970881'
    connection = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER=' +
                                server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD=' + password)
    cursor = connection.cursor()

    # save each label in the data base
    format_str = """UPDATE songs SET label = {label} WHERE id={id};"""
    for i in range(0,len(labels)):
        sql_command = format_str.format(label=labels[i], id=ids[i])
        cursor.execute(sql_command)
        print('Label'+str(i)+' in DB geschrieben')
    connection.commit()