import itertools
import json
import random

import numpy as np
from sklearn import metrics
from sklearn.cluster import KMeans

from constants import CP, MSD_DATA_LABELED_FILE_PATH, PARS
from listening_count_reader import get_random_test_listeners
from recommender import test_recommend
from song_dict_reader import read_song_dict_wo_labels


def add_kmeans_labels():
    '''
    Reads the song data file without clustering labels, then calls kmeans++
    clustering and saves the data including the clustering label results in
    another file.
    For clustering, 200 centroids and the parameters timeSig, songkey and mode
    are chosen because that combination had the best testing results.
    '''
    song_dict = read_song_dict_wo_labels()
    keys = []
    cluster_list = []
    for key in song_dict:
        keys.append(key)
        cluster_list.append([song_dict[key][par] for par in CP])
    labels = do_kmeans(cluster_list, 200)[0]
    # save the labels and the new file
    for index in range(0, len(keys)):
        song_dict[keys[index]]['label'] = np.asscalar(labels[index])
    with open(MSD_DATA_LABELED_FILE_PATH, 'w') as outfile:
        json.dump(song_dict, outfile)


def do_kmeans(par_list, cluster_cnt):
    '''
    Executes a kmeans++ clustering with a specified amount of
    centroids and returns the labels as well as the cluster centroids.

    par_list: list containing the tupels to cluster

    cluster_cnt: the amount of clusters to be made
    '''
    kmeans = KMeans(n_clusters=cluster_cnt, init='k-means++')
    kmeans.fit(par_list)
    return kmeans.labels_, kmeans.cluster_centers_


def test_kmeans(limits):
    '''
    Tests different configurations for kmeans++ clustering - different
    amounts of centroids, different cluster parameters and different
    other parameters to use for point distribution - to see which one
    has the best silhouette score and point distribution.

    This was needed while developing the application and is not used
    for the recommender system.

    limits: list containing two int numbers - the limits between
    rating a song as bad, medium or good
    '''
    entered_ids, test_ids_bad, test_ids_medium, test_ids_good = \
        get_random_test_listeners(limits)
    song_dict = read_song_dict_wo_labels()
    par_combinations = []
    for i in range(3, len(PARS) + 1):
        listing = [list(x) for x in itertools.combinations(PARS, i)]
        par_combinations.extend(listing)
    # all combinations of cluster parameters
    for par_combination in par_combinations:
        ncp_total = [
            item for item in PARS if item not in par_combination]
        ncp_combinations = []
        for i in range(0, len(ncp_total) + 1):
            listing = [list(x) for x in itertools.combinations(ncp_total, i)]
            ncp_combinations.extend(listing)
        # all combinations of other parameters
        for ncp_combination in ncp_combinations:
            ids = []
            cluster_list = []
            for key in song_dict:
                ids.append(key)
                cluster_list.append([song_dict[key][par]
                                     for par in par_combination])
            # take a random sample of users
            rnd_user_indices = random.sample(
                range(0, len(entered_ids)), min(50, len(entered_ids)))
            # different amount of centroids
            for count in [5, 10, 25, 50, 100, 200]:
                print('\nk-means++ with k =', str(count))
                print('cluster parameters:', par_combination)
                print('other parameters:', ncp_combination)
                print('limits for bad/medium/good:', limits)
                labels, centroids = do_kmeans(cluster_list, count)
                for i in range(0, len(ids)):
                    song_dict[ids[i]]['label'] = labels[i]
                point_array_good = []
                point_array_medium = []
                point_array_bad = []
                # for each user, distribute points to all songs he listened to
                for index in rnd_user_indices:
                    test_ids = test_ids_good[index] + test_ids_bad[index] + \
                        test_ids_medium[index]
                    point_dict = test_recommend(
                        entered_ids[index], test_ids, song_dict, centroids)
                    for song_id in test_ids_good[index]:
                        point_array_good.append(point_dict[song_id])
                    for song_id in test_ids_medium[index]:
                        point_array_medium.append(point_dict[song_id])
                    for song_id in test_ids_bad[index]:
                        point_array_bad.append(point_dict[song_id])
                '''
                Silhouette Score is calculated as a measurement for how good
                the current clustering is. We calculate it 10 times and take
                the average.
                '''
                silhouettes = []
                for i in range(0, 10):
                    sil = metrics.silhouette_score(
                        cluster_list, labels, metric='euclidean',
                        sample_size=10000)
                    silhouettes.append(sil)
                # print results
                print('average Silhouette Score:', str(np.mean(silhouettes)))
                print('average points of the good songs:',
                      str(np.mean(point_array_good)),
                      str(len(point_array_good)))
                print('average points of the medium songs:',
                      str(np.mean(point_array_medium)),
                      str(len(point_array_medium)))
                print('average points of the bad songs:',
                      str(np.mean(point_array_bad)),
                      str(len(point_array_bad)))
