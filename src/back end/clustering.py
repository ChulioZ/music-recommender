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

server = 'mrd.database.windows.net'
database = 'mrd'
username = 'qaywsx'
password = 'w@970881'
connection = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER=' +
                            server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD=' + password)
cursor = connection.cursor()
param = "SELECT loudness,hotttnesss,tempo,timeSig,songkey,mode FROM songs"
cursor.execute(param)
paramResults = cursor.fetchall()
details = "SELECT title,artist FROM songs"
cursor.execute(details)
detailsResults = cursor.fetchall()

song_array = np.array(paramResults)

print song_array




kmeans = KMeans(n_clusters=35, init='k-means++')
kmeans.fit(song_array)

centroids = kmeans.cluster_centers_
labels = kmeans.labels_

print(centroids)
print(labels)
    
    
for i in labels:
        format_str = """INSERT INTO songs (label)
        VALUES ({label});"""
        sql_command = format_str.format(label = labels[i])
        cursor.execute(sql_command)    


connection.commit()
cursor.close()
connection.close()
