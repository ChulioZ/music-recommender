from db_song_getter import get_all_songinfos
from quark import get_centroid_distances
import math
import numpy as np


def recommend(entered_ids):
    song_array = get_all_songinfos(entered_ids=entered_ids)
    song_dict = {}
    for song in song_array:
        song_dict[song[0]] = {}
        song_dict[song[0]]['loudness'] = float(song[1])
        song_dict[song[0]]['hotttnesss'] = float(song[2])
        song_dict[song[0]]['tempo'] = float(song[3])
        song_dict[song[0]]['timeSig'] = float(song[4])
        song_dict[song[0]]['songkey'] = float(song[5])
        song_dict[song[0]]['mode'] = float(song[6])
        song_dict[song[0]]['label'] = int(float(song[7]))
        song_dict[song[0]]['points'] = 0
    clusters = {}
    for i in range(0, 35):
        cluster = []
        for song in song_dict:
            if song_dict[song]['label'] == i:
                cluster.append(song)
        clusters[i] = (cluster)
    print(clusters)
    for songid in entered_ids:
        max_distance = -float("inf")
        min_distance = float("inf")
        for sid in clusters[song_dict[songid]['label']]:
            clusters[song_dict[songid]['label']]
            if songid is not sid:
                distance = 0
                for key in ['loudness', 'hotttnesss', 'tempo', 'timeSig', 'songkey', 'mode']:
                    distance += math.pow(song_dict[songid]
                                         [key] - song_dict[sid][key], 2)
                song_dict[sid]['distance'] = distance
                max_distance = max(max_distance, distance)
                min_distance = min(min_distance, distance)
        for sid in clusters[song_dict[songid]['label']]:
            diff = max_distance - song_dict[sid]['distance']
            if(max_distance == min_distance):
                points = 8
            else:
                points = diff / (max_distance - min_distance) * 2 + 8
            song_dict[sid]['points'] = max(song_dict[sid]['points'], points)
        centr_distances = get_centroid_distances()
        distances = []
        for i in range(0, 35):
            if i != song_dict[songid]['label']:
                distances.append(
                    centr_distances[song_dict[songid]['label']]['distances'][i])
        avg_distance = np.mean(distances)
        for i in range(0, 35):
            if i != song_dict[songid]['label']:
                if centr_distances[song_dict[songid]['label']]['distances'][i] <= 0.1 * avg_distance:
                    max_distance = -float("inf")
                    min_distance = float("inf")
                    for sid in clusters[i]:
                        distance = 0
                        for key in ['loudness', 'hotttnesss', 'tempo', 'timeSig', 'songkey', 'mode']:
                            distance += math.pow(song_dict[songid]
                                                 [key] - song_dict[sid][key], 2)
                        song_dict[sid]['distance'] = distance
                        max_distance = max(max_distance, distance)
                        min_distance = min(min_distance, distance)
                    for sid in clusters[i]:
                        diff = max_distance - song_dict[sid]['distance']
                        if(max_distance == min_distance):
                            points = 6
                        else:
                            points = diff / (max_distance - min_distance) + 6
                        song_dict[sid]['points'] = max(
                            song_dict[sid]['points'], points)
                elif centr_distances[song_dict[songid]['label']]['distances'][i] <= 0.25 * avg_distance:
                    max_distance = -float("inf")
                    min_distance = float("inf")
                    for sid in clusters[i]:
                        distance = 0
                        for key in ['loudness', 'hotttnesss', 'tempo', 'timeSig', 'songkey', 'mode']:
                            distance += math.pow(song_dict[songid]
                                                 [key] - song_dict[sid][key], 2)
                        song_dict[sid]['distance'] = distance
                        max_distance = max(max_distance, distance)
                        min_distance = min(min_distance, distance)
                    for sid in clusters[i]:
                        diff = max_distance - song_dict[sid]['distance']
                        if(max_distance == min_distance):
                            points = 4
                        else:
                            points = diff / (max_distance - min_distance) + 4
                        song_dict[sid]['points'] = max(
                            song_dict[sid]['points'], points)
                elif centr_distances[song_dict[songid]['label']]['distances'][i] <= 0.5 * avg_distance:
                    max_distance = -float("inf")
                    min_distance = float("inf")
                    for sid in clusters[i]:
                        distance = 0
                        for key in ['loudness', 'hotttnesss', 'tempo', 'timeSig', 'songkey', 'mode']:
                            distance += math.pow(song_dict[songid]
                                                 [key] - song_dict[sid][key], 2)
                        song_dict[sid]['distance'] = distance
                        max_distance = max(max_distance, distance)
                        min_distance = min(min_distance, distance)
                    for sid in clusters[i]:
                        diff = max_distance - song_dict[sid]['distance']
                        if(max_distance == min_distance):
                            points = 2
                        else:
                            points = diff / (max_distance - min_distance) + 2
                        song_dict[sid]['points'] = max(
                            song_dict[sid]['points'], points)
                else:
                    for sid in clusters[i]:
                        song_dict[sid]['points'] = max(
                            song_dict[sid]['points'], 0)
    return song_dict

def test_recommend(ids2test):
    x = 0