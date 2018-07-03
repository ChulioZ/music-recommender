from db_song_getter import get_all_songinfos, get_all_centroids
from centroid_distance_getter import get_centroid_distances
from clustering import do_kmeans
import math
import numpy as np
from functools import reduce
from song_dict_reader import read_song_dict_w_labels
import operator
from numpy import linalg as LA


def recommend(song_dict, entered_ids, amount):
    clusters = build_song_clusters(song_dict, 200)
    for songid in entered_ids:
        ids_to_give_points = [
            sid for sid in clusters[song_dict[songid]['label']] if sid not in entered_ids]
        song_dict = distribute_points(
            ids_to_give_points, song_dict, songid)
    point_dict = build_point_dict(song_dict)
    print('You entered the following songs ...')
    for entered_id in entered_ids:
        print(song_dict[entered_id]['title'], 'by',
              song_dict[entered_id]['artist'])
    print('\nThese are the best ' + str(amount) + ' songs you might also like:')
    for i in range(0, amount):
        best_song = max(point_dict.items(), key=operator.itemgetter(1))[0]
        print(song_dict[best_song]['title'], 'by',
              song_dict[best_song]['artist'], '(' + str(point_dict[best_song]) + ' points)')
        point_dict.pop(best_song)


def test_recommend(entered_ids, ids2test, cp, ncp, song_dict, centroids):
    clusters = build_song_clusters(song_dict, len(centroids))
    centr_distances = get_centroid_distances(centroids, cp)
    for songid in entered_ids:
        song_label = song_dict[songid]['label']
        distances = []
        for i in range(0, len(centroids)):
            if i != song_label:
                distances.append(
                    centr_distances[song_label]['distances'][i])
        avg_distance = np.mean(distances)
        for i in range(0, len(centroids)):
            if i == song_label:
                song_dict = distribute_test_points(
                    list(reduce(set.intersection, map(set, [clusters[i], ids2test]))), song_dict, songid, 8, 10, cp, ncp)
            elif centr_distances[song_label]['distances'][i] <= 0.1 * avg_distance:
                song_dict = distribute_test_points(
                    list(reduce(set.intersection, map(set, [clusters[i], ids2test]))), song_dict, songid, 6, 7, cp, ncp)
            elif centr_distances[song_label]['distances'][i] <= 0.25 * avg_distance:
                song_dict = distribute_test_points(
                    list(reduce(set.intersection, map(set, [clusters[i], ids2test]))), song_dict, songid, 4, 5, cp, ncp)
            elif centr_distances[song_label]['distances'][i] <= 0.5 * avg_distance:
                song_dict = distribute_test_points(
                    list(reduce(set.intersection, map(set, [clusters[i], ids2test]))), song_dict, songid, 2, 3, cp, ncp)
    point_dict = build_point_dict(song_dict)
    return point_dict


def build_song_clusters(song_dict, count):
    clusters = {}
    for i in range(0, count):
        cluster = []
        for song in song_dict:
            if song_dict[song]['label'] == i:
                cluster.append(song)
        clusters[i] = cluster
    return clusters


def distribute_points(ids_to_give_points, song_dict, entered_id):
    max_points = 10
    min_points = 8
    distances = []
    ncp_distances = []
    cp = ['timeSig', 'songkey', 'mode']
    ncp = ['loudness', 'tempo']
    for sid in ids_to_give_points:
        if sid is not entered_id:
            par_distances = [song_dict[entered_id][key] -
                             song_dict[sid][key] for key in cp]
            distance = LA.norm(par_distances, 2)
            song_dict[sid]['distance'] = distance
            distances.append(distance)
            ncp_par_distances = [song_dict[entered_id][key] -
                                 song_dict[sid][key] for key in ncp]
            ncp_distance = LA.norm(ncp_par_distances, 2)
            song_dict[sid]['ncpdistance'] = ncp_distance
            ncp_distances.append(ncp_distance)
    max_distance = max(distances)
    min_distance = min(distances)
    max_ncp_distance = max(ncp_distances)
    min_ncp_distance = min(ncp_distances)
    for sid in ids_to_give_points:
        if(max_distance == min_distance):
            points = max_points
        else:
            diff = max_distance - song_dict[sid]['distance']
            points = diff / (max_distance - min_distance) * \
                (max_points - min_points) + min_points
        points *= len(cp)/(len(cp) + len(ncp))
        if(max_ncp_distance == min_ncp_distance):
            ncp_points = max_points
        else:
            diff = max_ncp_distance - song_dict[sid]['ncpdistance']
            ncp_points = diff / (max_ncp_distance - min_ncp_distance) * \
                (max_points - min_points) + min_points
        ncp_points *= len(ncp)/(len(cp) + len(ncp))
        song_dict[sid]['points'] = max(
            song_dict[sid]['points'], points + ncp_points)
    return song_dict


def distribute_test_points(ids_in_cluster, song_dict, songid, min_points, max_points, cp, ncp):
    distances = []
    ncp_distances = []
    for key in ncp:
        ncp_distances.append([])
    for sid in ids_in_cluster:
        if sid is not songid:
            par_distances = [song_dict[songid][key] -
                             song_dict[sid][key] for key in cp]
            distance = LA.norm(par_distances, 2)
            song_dict[sid]['distance'] = distance
            distances.append(distance)
            for i in range(0, len(ncp)):
                ncp_distances[i].extend(
                    [math.pow(song_dict[songid][ncp[i]] - song_dict[sid][ncp[i]], 2)])
    max_distance = max(distances)
    min_distance = min(distances)
    ncp_distance_means = [np.mean(index) for index in ncp_distances]
    for sid in ids_in_cluster:
        if(max_distance == min_distance):
            points = max_points
        else:
            diff = max_distance - song_dict[sid]['distance']
            points = diff / (max_distance - min_distance) * \
                (max_points - min_points) + min_points
        points *= len(cp)/(len(cp) + len(ncp))
        for i in range(0, len(ncp)):
            dist = math.pow(song_dict[songid]
                            [ncp[i]] - song_dict[sid][ncp[i]], 2)
            if dist == 0:
                points += 1/(len(cp) + len(ncp))*max_points
            elif dist <= 0.1 * ncp_distance_means[i]:
                points += 1/(2 * (len(cp) + len(ncp)))*max_points
            elif dist <= 0.5 * ncp_distance_means[i]:
                points += 1/(4 * (len(cp) + len(ncp)))*max_points
        song_dict[sid]['points'] = max(song_dict[sid]['points'], points)
    return song_dict


def build_point_dict(song_dict):
    point_dict = {}
    for song in song_dict:
        point_dict[song] = song_dict[song]['points']
    return point_dict
