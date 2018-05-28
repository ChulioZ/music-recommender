import os
import time
import datetime
import glob
import math
import numpy as np
from sklearn.cluster import KMeans
import hdf5_getters as GETTERS
import pyodbc
from os.path import dirname, abspath
from mice import MICE


def do_kmeans():
    start = time.time()

    server = 'mrd.database.windows.net'
    database = 'mrd'
    username = 'qaywsx'
    password = 'w@970881'
    connection = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER=' +
                                server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD=' + password)
    cursor = connection.cursor()

    print('Hole Parameter')
    param = "SELECT loudness,hotttnesss,tempo,timeSig,songkey,mode FROM songs"
    cursor.execute(param)
    paramResults = cursor.fetchall()
    song_array = np.array(paramResults)
    print(str(datetime.timedelta(seconds=time.time()-start)))

    print('Hole IDs')
    ids = "SELECT id FROM songs"
    cursor.execute(ids)
    idsResults = cursor.fetchall()
    id_array = np.array(idsResults)
    print(id_array[3][0])
    print(str(datetime.timedelta(seconds=time.time()-start)))

    print('Führe k-means++ aus')
    kmeans = KMeans(n_clusters=35, init='k-means++')
    kmeans.fit(song_array)
    print(str(datetime.timedelta(seconds=time.time()-start)))

    centroids = kmeans.cluster_centers_
    format_strc = """INSERT INTO centroids (label, loudness, hotttnesss, tempo, timeSig, songkey, mode)
                VALUES ({label}, {loudness}, {hotttnesss}, {tempo}, {timeSig}, {songkey}, {mode});"""
    for i in range(0, len(centroids)):
        sql_command = format_strc.format(label=i, loudness=centroids[i][0], hotttnesss=centroids[i][1],
                                         tempo=centroids[i][2], timeSig=centroids[i][3], songkey=centroids[i][4], mode=centroids[i][5])
        cursor.execute(sql_command)
        print('centroid'+str(i)+'eingetragen')
    print(str(datetime.timedelta(seconds=time.time()-start)))

    labels = kmeans.labels_
    format_strl = """UPDATE songs SET label = {label} WHERE id = '{id}';"""
    for i in range(0, len(labels)):
        sql_command = format_strl.format(label=labels[i], id=id_array[i][0])
        cursor.execute(sql_command)
        print('label'+str(i)+'eingetragen')

    connection.commit()
    cursor.close()
    connection.close()
    print(str(datetime.timedelta(seconds=time.time()-start)))
