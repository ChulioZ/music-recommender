from db_song_getter import get_all_songinfos, get_all_centroids
from centroid_distance_getter import get_centroid_distances
from clustering import do_kmeans
import math
import numpy as np
from functools import reduce
from kmeans_tester import read_song_dict_w_labels


def recommend(entered_ids):
    song_dict = read_song_dict_w_labels()
    clusters = build_song_clusters(song_dict, 200)
    cp = ['timeSig', 'songkey', 'mode']
    ncp = []
    for songid in entered_ids:
        song_dict = distribute_points(
            clusters[song_dict[songid]['label']], song_dict, songid, 8, 10, cp, ncp)
    point_dict = build_point_dict(song_dict)
    return point_dict


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
                song_dict = distribute_points(
                    list(reduce(set.intersection, map(set, [clusters[i], ids2test]))), song_dict, songid, 8, 10, cp, ncp)
            elif centr_distances[song_label]['distances'][i] <= 0.1 * avg_distance:
                song_dict = distribute_points(
                    list(reduce(set.intersection, map(set, [clusters[i], ids2test]))), song_dict, songid, 6, 7, cp, ncp)
            elif centr_distances[song_label]['distances'][i] <= 0.25 * avg_distance:
                song_dict = distribute_points(
                    list(reduce(set.intersection, map(set, [clusters[i], ids2test]))), song_dict, songid, 4, 5, cp, ncp)
            elif centr_distances[song_label]['distances'][i] <= 0.5 * avg_distance:
                song_dict = distribute_points(
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


def distribute_points(ids_in_cluster, song_dict, songid, min_points, max_points, cp, ncp):
    max_distance = -float("inf")
    min_distance = float("inf")
    ncp_distances = []
    for key in ncp:
        ncp_distances.append([])
    for sid in ids_in_cluster:
        if sid is not songid:
            distance = 0
            for key in cp:
                distance += math.pow(song_dict[songid]
                                     [key] - song_dict[sid][key], 2)
            distance = math.sqrt(distance)
            song_dict[sid]['distance'] = distance
            max_distance = max(max_distance, distance)
            min_distance = min(min_distance, distance)
            for i in range(0, len(ncp)):
                ncp_distances[i].extend(
                    [song_dict[songid][ncp[i]] - song_dict[sid][ncp[i]]])
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
            if song_dict[songid][ncp[i]] == song_dict[sid][ncp[i]]:
                points += 1/(len(cp) + len(ncp))*max_points
            elif song_dict[songid][ncp[i]] - song_dict[sid][ncp[i]] <= 0.1 * ncp_distance_means[i]:
                points += 1/(2 * (len(cp) + len(ncp)))*max_points
        song_dict[sid]['points'] = max(song_dict[sid]['points'], points)
    return song_dict


def build_point_dict(song_dict):
    point_dict = {}
    for song in song_dict:
        point_dict[song] = song_dict[song]['points']
    return point_dict
