import pyodbc
import math
import numpy as np


def d():
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
        distances = []
        for j in range(0, 35):
            if index != j:
                distance = 0
                for key in ['loudness', 'hotttnesss', 'tempo', 'timeSig', 'songkey', 'mode']:
                    distance += math.pow(centroids[index]
                                         [key] - centroids[j][key], 2)
                distances.append(distance)
        centroids[index]['distances'] = distances

    song_centroids = []
    centroid_sql = """SELECT label FROM songs WHERE id='{id}';"""
    for song_id in ['SOMAKIT12A58A7E292', 'SOPSAIO12A58A7AE45', 'SOHXDYZ12A8C145925', 'SOCRCNK12A8C133AA7', 'SOYRSUR12A6D4FB19B']:
        sql_req = centroid_sql.format(id=song_id)
        cursor.execute(sql_req)
        centroid_results = cursor.fetchall()
        song_centroids.append(int(round(centroid_results[0][0])))

    for center in song_centroids:
        print('Median für Zentrum '+str(center)+': ' +
              str(np.mean(centroids[center]['distances'])))
        distances = []
        for c in song_centroids:
            if center < c:
                distances.append(centroids[center]['distances'][c-1])
                print('Abstand zum Zentrum '+str(c)+': ' +
                      str(centroids[center]['distances'][c-1]))
            if center > c:
                distances.append(centroids[center]['distances'][c])
                print('Abstand zum Zentrum '+str(c)+': ' +
                      str(centroids[center]['distances'][c]))
        print('Durchschnittlicher Abstand zu anderen Zentren der gehörten Songs: '+str(np.mean(distances)))
        print('\n')