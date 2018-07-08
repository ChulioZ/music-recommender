from numpy import linalg as LA

from constants import CP


def get_centroid_distances(centroids):
    '''
    Returns a dictionary containing the centroids' distances to all
    other centroids.

    centroids: List of centroids as returned by kmeans centroids
    '''
    centroid_distances = {}
    for index in range(0, len(centroids)):
        distances = {}
        for j in range(0, len(centroids)):
            if index != j:
                # Calculate and save the distance to centroid j
                par_distances = [centroid_distances[index][key]
                                 - centroid_distances[j][key] for key in CP]
                distances[j] = LA.norm(par_distances, 2)  # euclidean distance
        centroid_distances[index] = distances
    return centroid_distances
