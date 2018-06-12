import pyodbc
import math
import numpy as np


def get_centroid_distances(centroids, cp):
    centroid_distances = {}
    for j in range(0, len(centroids)):
        centroid_distances[j] = {}
        for i in range(0, len(cp)):
            centroid_distances[j][cp[i]] = centroids[j][i]

    for index in range(0, len(centroids)):
        distances = {}
        for j in range(0, len(centroids)):
            if index != j:
                distance = 0
                for key in cp:
                    distance += math.pow(centroid_distances[index]
                                         [key] - centroid_distances[j][key], 2)
                distances[j] = math.sqrt(distance)
        centroid_distances[index]['distances'] = distances

    return centroid_distances