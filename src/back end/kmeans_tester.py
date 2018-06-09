from clustering import do_kmeans
from db_song_getter import get_all_cluster_parameters, get_all_other_parameters, get_all_ids
from recommender import test_recommend
import numpy as np
import random
from sklearn import metrics


def test_kmeans(entered_ids, test_ids_good, test_ids_bad):
    ids = get_all_ids()
    cluster_parameters = get_all_cluster_parameters()
    other_parameters = get_all_other_parameters()
    print('\n')
    for i in range(0, 3):
        rnd_users = random.sample(
            range(0, len(entered_ids)), min(25, len(entered_ids)))
        for count in [10, 25, 35, 50, 100]:
            print('Führe k-means++-Test mit ' +
                  str(count)+' Cluster-Zentren aus...\n')
            labels, centroids = do_kmeans(cluster_parameters, count)
            song_dict = build_song_dict(
                ids, cluster_parameters, other_parameters, labels)
            point_array_good = []
            point_array_bad = []
            cnt_cluster_0_good = 0
            cnt_cluster_10_good = 0
            cnt_cluster_25_good = 0
            cnt_cluster_away_good = 0
            cnt_cluster_0_bad = 0
            cnt_cluster_10_bad = 0
            cnt_cluster_25_bad = 0
            cnt_cluster_away_bad = 0
            for index in rnd_users:
                point_dict = test_recommend(
                    entered_ids[index], test_ids_good[index], centroids=centroids, song_dict=song_dict)
                for song_id in test_ids_good[index]:
                    points = point_dict[song_id]
                    point_array_good.append(points)
                    if points >= 8:
                        cnt_cluster_0_good += 1
                    elif points >= 6:
                        cnt_cluster_10_good += 1
                    elif points >= 4:
                        cnt_cluster_25_good += 1
                    else:
                        cnt_cluster_away_good += 1
            for index in rnd_users:
                point_dict = test_recommend(
                    entered_ids[index], test_ids_bad[index], centroids=centroids, song_dict=song_dict)
                for song_id in test_ids_bad[index]:
                    points = point_dict[song_id]
                    point_array_bad.append(points)
                    if points >= 8:
                        cnt_cluster_0_bad += 1
                    elif points >= 6:
                        cnt_cluster_10_bad += 1
                    elif points >= 4:
                        cnt_cluster_25_bad += 1
                    else:
                        cnt_cluster_away_bad += 1
            print('Ergebnisse für k-means++ mit ' + str(count) +
                  ' Cluster-Zentren, Durchlauf ' + str(i+1)+':')
            silhouettes = []
            for i in range(0, 10):
                sil = metrics.silhouette_score(
                    cluster_parameters, labels, metric='euclidean', sample_size=10000)
                silhouettes.append(sil)
                print('Silhouette Score Nr. ' + str(i) + ': ' + str(sil))
            print('Durschnittliche Silhouette Score: ' +
                  str(np.mean(silhouettes)))
            print('Durchschnittliche Punktzahl der gemochten Songs: ' +
                  str(np.mean(point_array_good)))
            print('Durchschnittliche Punktzahl der nicht gemochten Songs: ' +
                  str(np.mean(point_array_bad)))
            print('Erfolgsquote für selbes Cluster der gemochten Songs: ' + str(cnt_cluster_0_good /
                                                                                (cnt_cluster_0_good + cnt_cluster_10_good + cnt_cluster_25_good + cnt_cluster_away_good) * 100) + ' %')
            print('Erfolgsquote für selbes Cluster der nicht gemochten Songs: ' + str(cnt_cluster_0_bad /
                                                                                      (cnt_cluster_0_bad + cnt_cluster_10_bad + cnt_cluster_25_bad + cnt_cluster_away_bad) * 100) + ' %')
            print('Erfolgsquote für 10-%-Mean-Cluster der gemochten Songs: ' + str(cnt_cluster_10_good /
                                                                                   (cnt_cluster_0_good + cnt_cluster_10_good + cnt_cluster_25_good + cnt_cluster_away_good) * 100) + ' %')
            print('Erfolgsquote für 10-%-Mean-Cluster der nicht gemochten Songs: ' + str(cnt_cluster_10_bad /
                                                                                         (cnt_cluster_0_bad + cnt_cluster_10_bad + cnt_cluster_25_bad + cnt_cluster_away_bad) * 100) + ' %')
            print('Erfolgsquote für 25-%-Mean-Cluster der gemochten Songs: ' + str(cnt_cluster_25_good /
                                                                                   (cnt_cluster_0_good + cnt_cluster_10_good + cnt_cluster_25_good + cnt_cluster_away_good) * 100) + ' %')
            print('Erfolgsquote für 25-%-Mean-Cluster der nicht gemochten Songs: ' + str(cnt_cluster_25_bad /
                                                                                         (cnt_cluster_0_bad + cnt_cluster_10_bad + cnt_cluster_25_bad + cnt_cluster_away_bad) * 100) + ' %')
            print('\n\n')


def build_song_dict(ids, cluster_parameters, other_parameters, labels):
    song_dict = {}
    for song in range(0, len(ids)):
        song_id = ids[song][0]
        song_dict[song_id] = {}
        song_dict[song_id]['loudness'] = cluster_parameters[song][0]
        song_dict[song_id]['hotttnesss'] = cluster_parameters[song][1]
        song_dict[song_id]['tempo'] = cluster_parameters[song][2]
        song_dict[song_id]['timeSig'] = cluster_parameters[song][3]
        song_dict[song_id]['songkey'] = cluster_parameters[song][4]
        song_dict[song_id]['mode'] = other_parameters[song][0]
        song_dict[song_id]['label'] = labels[song]
        song_dict[song_id]['points'] = 0
    return song_dict
