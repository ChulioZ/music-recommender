from clustering import do_kmeans
from db_song_getter import get_specific_parameters, get_all_ids
from recommender import test_recommend
import numpy as np
import random
from sklearn import metrics
import itertools


def test_kmeans(entered_ids, test_ids_good, test_ids_bad):
    ids = get_all_ids()
    parameters = ['loudness', 'hotttnesss', 'tempo', 'timeSig', 'songkey', 'mode']
    par_combinations = []
    for i in range(3, len(parameters) + 1):
        listing = [list(x) for x in itertools.combinations(parameters, i)]
        par_combinations.extend(listing)
    for cp in par_combinations:
        ncp = [item for item in parameters if item not in cp]
        cluster_parameters = get_specific_parameters(cp)
        other_parameters = get_specific_parameters(ncp)
        print('\n')
        rnd_users = random.sample(
            range(0, len(entered_ids)), min(25, len(entered_ids)))
        for count in [10, 25, 50, 100, 200]:
            print('Führe k-means++-Test mit ' +
                    str(count)+' Cluster-Zentren und folgenden Cluster-Parametern aus...\n')
            print('Cluster-Parameter: ', cp)
            labels, centroids = do_kmeans(cluster_parameters, count)
            song_dict = build_song_dict(
                ids, parameters, cp, ncp, cluster_parameters, other_parameters, labels)
            point_array_good = []
            point_array_bad = []
            for index in rnd_users:
                test_ids = test_ids_good[index] + test_ids_bad[index]
                point_dict = test_recommend(
                    entered_ids[index], test_ids, cp, ncp, centroids=centroids, song_dict=song_dict)
                for song_id in test_ids_good[index]:
                    points = point_dict[song_id]
                    point_array_good.append(points)
                for song_id in test_ids_bad[index]:
                    points = point_dict[song_id]
                    point_array_bad.append(points)
            print('Ergebnisse für k-means++ mit ' + str(count) +
                    ' Cluster-Zentren, Durchlauf ' + str(i+1)+':')
            silhouettes = []
            for i in range(0, 10):
                sil = metrics.silhouette_score(
                    cluster_parameters, labels, metric='euclidean', sample_size=10000)
                silhouettes.append(sil)
            print('Durschnittliche Silhouette Score: ' +
                    str(np.mean(silhouettes)))
            print('Durchschnittliche Punktzahl der gemochten Songs: ' +
                    str(np.mean(point_array_good)))
            print('Durchschnittliche Punktzahl der nicht gemochten Songs: ' +
                    str(np.mean(point_array_bad)))
            print('\n\n')


def build_song_dict(ids, parameters, cp, ncp, cluster_parameters, other_parameters, labels):
    song_dict = {}
    for song in range(0, len(ids)):
        song_id = ids[song][0]
        song_dict[song_id] = {}
        for par in parameters:
            if par in cp:
                song_dict[song_id][par] = cluster_parameters[song][cp.index(par)]
            else:
                song_dict[song_id][par] = cluster_parameters[song][ncp.index(par)]
        song_dict[song_id]['label'] = labels[song]
        song_dict[song_id]['points'] = 0
    return song_dict
