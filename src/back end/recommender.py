import math
import operator
from functools import reduce

import numpy as np
from numpy import linalg as LA
from sklearn.ensemble import RandomForestClassifier

from centroid_distance_getter import get_centroid_distances
from listening_count_reader import get_listened_songs
from song_dict_reader import read_song_dict_w_labels


def recommend(song_dict, entered_ids, amount):
    clusters = build_song_clusters(song_dict, 200)
    for song_id in entered_ids:
        ids_to_give_points = [
            sid for sid in clusters[song_dict[song_id]['label']] if sid not in entered_ids]
        song_dict = distribute_points(
            ids_to_give_points, song_dict, song_id)
    print_recommendation(song_dict, entered_ids, amount)


def recommend_w_rf(song_dict, entered_ids, amount):
    rf_ids = []
    rf_pars = []
    rf_targets = []
    listened_songs = get_listened_songs(limits=[9, 24])[0]
    for user in listened_songs.keys():
        contains_good_song = False
        for song_id in entered_ids:
            contains_good_song = song_id in listened_songs[user]['good']
        if contains_good_song:
            for like in ['bad', 'medium', 'good']:
                for song_id in listened_songs[user][like]:
                    if song_id not in rf_ids:
                        rf_ids.append(song_id)
                        rf_pars.append([song_dict[song_id][par] for par in [
                                       'loudness', 'hotttnesss', 'tempo', 'timeSig', 'songkey', 'mode']])
                        rf_targets.append(like)
                    elif (rf_targets[rf_ids.index(song_id)] == 'bad') or (rf_targets[rf_ids.index(song_id)] == 'medium' and like == 'good'):
                        rf_targets[rf_ids.index(song_id)] = like
    rf = RandomForestClassifier()
    rf.fit(rf_pars, rf_targets)
    ids = []
    songs_to_predict = []
    for song_id in song_dict:
        songs_to_predict.append([song_dict[song_id][par] for par in [
                                'loudness', 'hotttnesss', 'tempo', 'timeSig', 'songkey', 'mode']])
        ids.append(song_id)
    predictions = rf.predict(songs_to_predict)
    good_indices = []
    for i in range(0, len(predictions)):
        if predictions[i] == 'good':
            good_indices.append(i)
    ids_to_give_points = [ids[index]
                          for index in good_indices if ids[index] not in entered_ids]
    song_dict = distribute_points(ids_to_give_points, song_dict, song_id)
    print_recommendation(song_dict, entered_ids, amount)


def print_recommendation(song_dict, entered_ids, amount):
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


def test_recommend(entered_ids, ids2test, song_dict, centroids):
    clusters = build_song_clusters(song_dict, len(centroids))
    centr_distances = get_centroid_distances(centroids)
    for song_id in entered_ids:
        song_label = song_dict[song_id]['label']
        distances = []
        for i in range(0, len(centroids)):
            if i != song_label:
                distances.append(
                    centr_distances[song_label]['distances'][i])
        avg_distance = np.mean(distances)
        for i in range(0, len(centroids)):
            if i == song_label:
                song_dict = distribute_points(
                    list(reduce(set.intersection, map(set, [clusters[i], ids2test]))), song_dict, song_id)
            elif centr_distances[song_label]['distances'][i] <= 0.1 * avg_distance:
                song_dict = distribute_points(
                    list(reduce(set.intersection, map(set, [clusters[i], ids2test]))), song_dict, song_id, min_points=6, max_points=7)
            elif centr_distances[song_label]['distances'][i] <= 0.25 * avg_distance:
                song_dict = distribute_points(
                    list(reduce(set.intersection, map(set, [clusters[i], ids2test]))), song_dict, song_id, min_points=4, max_points=5)
            elif centr_distances[song_label]['distances'][i] <= 0.5 * avg_distance:
                song_dict = distribute_points(
                    list(reduce(set.intersection, map(set, [clusters[i], ids2test]))), song_dict, song_id, min_points=2, max_points=3)
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


def distribute_points(ids_to_give_points, song_dict, entered_id, min_points=8, max_points=10):
    if not ids_to_give_points:
        return song_dict
    distances = []
    pars = ['timeSig', 'songkey', 'mode', 'loudness', 'tempo']
    for sid in ids_to_give_points:
        if sid is not entered_id:
            par_distances = [song_dict[entered_id][key] -
                             song_dict[sid][key] for key in pars]
            distance = LA.norm(par_distances, 2)
            song_dict[sid]['distance'] = distance
            distances.append(distance)
    max_distance = max(distances)
    min_distance = min(distances)
    for sid in ids_to_give_points:
        if(max_distance == min_distance):
            points = max_points
        else:
            diff = max_distance - song_dict[sid]['distance']
            points = diff / (max_distance - min_distance) * \
                (max_points - min_points) + min_points
        song_dict[sid]['points'] = max(
            song_dict[sid]['points'], points)
    return song_dict


def build_point_dict(song_dict):
    point_dict = {}
    for song in song_dict:
        point_dict[song] = song_dict[song]['points']
    return point_dict
