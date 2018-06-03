import pyodbc
import math
import numpy as np


def get_centroid_distances(centroids):
    centroid_distances = {}
    for j in range(0, len(centroids)):
        centroid_distances[j] = {}
        centroid_distances[j]['loudness'] = centroids[j][0]
        centroid_distances[j]['hotttnesss'] = centroids[j][1]
        centroid_distances[j]['tempo'] = centroids[j][2]
        centroid_distances[j]['timeSig'] = centroids[j][3]
        centroid_distances[j]['songkey'] = centroids[j][4]

    for index in range(0, len(centroids)):
        distances = {}
        for j in range(0, len(centroids)):
            if index != j:
                distance = 0
                for key in ['loudness', 'hotttnesss', 'tempo', 'timeSig', 'songkey']:
                    distance += math.pow(centroid_distances[index]
                                         [key] - centroid_distances[j][key], 2)
                distances[j] = math.sqrt(distance)
        centroid_distances[index]['distances'] = distances

    return centroid_distances