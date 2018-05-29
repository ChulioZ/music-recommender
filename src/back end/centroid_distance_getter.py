import pyodbc
import math
import numpy as np


def get_centroid_distances():
    server = 'mrd.database.windows.net'
    database = 'mrd'
    username = 'qaywsx'
    password = 'w@970881'
    connection = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER=' +
                                server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD=' + password)
    cursor = connection.cursor()

    param = "SELECT loudness,hotttnesss,tempo,timeSig,songkey,mode FROM centroids"
    cursor.execute(param)
    paramResults = cursor.fetchall()

    centroids = {}
    for j in range(0, 35):
        centroids[j] = {}
        centroids[j]['loudness'] = float(paramResults[j][0])
        centroids[j]['hotttnesss'] = float(paramResults[j][1])
        centroids[j]['tempo'] = float(paramResults[j][2])
        centroids[j]['timeSig'] = float(paramResults[j][3])
        centroids[j]['songkey'] = float(paramResults[j][4])
        centroids[j]['mode'] = float(paramResults[j][5])

    for key in ['loudness', 'hotttnesss', 'tempo', 'timeSig', 'songkey', 'mode']:
        max_value = -float("inf")
        min_value = float("inf")
        for index in range(0, 35):
            max_value = max(max_value, float(centroids[index][key]))
            min_value = min(min_value, float(centroids[index][key]))
        for index in range(0, 35):
            centroids[index][key] = (
                float(centroids[index][key]) - min_value)/(max_value - min_value) * 100

    for index in range(0, 35):
        distances = {}
        for j in range(0, 35):
            if index != j:
                distance = 0
                for key in ['loudness', 'hotttnesss', 'tempo', 'timeSig', 'songkey', 'mode']:
                    distance += math.pow(centroids[index]
                                         [key] - centroids[j][key], 2)
                distances[j] = distance
        centroids[index]['distances'] = distances

    return centroids