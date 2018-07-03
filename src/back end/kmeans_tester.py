from clustering import do_kmeans
from db_song_getter import get_specific_parameters, get_all_ids
from recommender import test_recommend
import numpy as np
import random
from sklearn import metrics
import itertools
from os.path import dirname, abspath
import json


file_path = dirname(dirname(dirname(abspath(__file__))))


def read_song_dict_wo_labels():
    with open(file_path + '/msd_data.txt', 'r') as f:
        song_dict = json.load(f)
    return build_song_dict(song_dict)


def read_song_dict_w_labels():
    with open(file_path + '/msd_data_labeled.txt', 'r') as f:
        song_dict = json.load(f)
    return build_song_dict(song_dict)


def add_kmeans_labels():
    song_dict = read_song_dict_wo_labels()
    ids = []
    cluster_parameters = []
    cp = ['timeSig', 'songkey', 'mode']
    ncp = []
    for key in song_dict:
        ids.append(key)
        cluster_parameters.append([song_dict[key][par] for par in cp])
    labels, centroids = do_kmeans(cluster_parameters, 200)
    for i in range(0, len(ids)):
        song_dict[ids[i]]['label'] = labels[i]
    with open(file_path + '/msd_data_labeled.txt', 'w') as outfile:
        json.dump(song_dict, outfile)


def test_kmeans(listened_songs, limits):
    entered_ids, test_ids_bad, test_ids_medium, test_ids_good, test_ids_super = get_listening_ids(
        listened_songs)
    song_dict = read_song_dict_wo_labels()
    parameters = ['loudness', 'hotttnesss',
                  'tempo', 'timeSig', 'songkey', 'mode']
    '''par_combinations = []
    for i in range(4, len(parameters) + 1):
        listing = [list(x) for x in itertools.combinations(parameters, i)]
        par_combinations.extend(listing)'''
    par_combinations = [['timeSig', 'songkey', 'mode']]
    for cp in par_combinations:
        ncp_total = [item for item in parameters if item not in cp]
        ncp_combinations = []
        for i in range(0, len(ncp_total) + 1):
            listing = [list(x) for x in itertools.combinations(ncp_total, i)]
            ncp_combinations.extend(listing)
        for ncp in ncp_combinations:
            ids = []
            cluster_parameters = []
            for key in song_dict:
                ids.append(key)
                cluster_parameters.append([song_dict[key][par] for par in cp])
            rnd_user_indices = random.sample(
                range(0, len(entered_ids)), min(50, len(entered_ids)))
            for count in [200]:
                print('\nk-means++ mit k =', str(count))
                print('Cluster-Parameter:', cp)
                print('Andere Parameter:', ncp)
                print('Limits für bad/medium/good/super:', limits)
                labels, centroids = do_kmeans(cluster_parameters, count)
                for i in range(0, len(ids)):
                    song_dict[ids[i]]['label'] = labels[i]
                point_array_super = []
                point_array_good = []
                point_array_medium = []
                point_array_bad = []
                for index in rnd_user_indices:
                    test_ids = test_ids_good[index] + test_ids_bad[index] + \
                        test_ids_medium[index] + test_ids_super[index]
                    point_dict = test_recommend(
                        entered_ids[index], test_ids, cp, ncp, song_dict, centroids)
                    for song_id in test_ids_super[index]:
                        point_array_super.append(point_dict[song_id])
                    for song_id in test_ids_good[index]:
                        point_array_good.append(point_dict[song_id])
                    for song_id in test_ids_medium[index]:
                        point_array_medium.append(point_dict[song_id])
                    for song_id in test_ids_bad[index]:
                        point_array_bad.append(point_dict[song_id])
                silhouettes = []
                for i in range(0, 10):
                    sil = metrics.silhouette_score(
                        cluster_parameters, labels, metric='euclidean', sample_size=10000)
                    silhouettes.append(sil)
                print('Durchschnittliche Silhouette Score: ' +
                    str(np.mean(silhouettes)))
                print('Durchschnittliche Punktzahl der super Songs: ' +
                    str(np.mean(point_array_super)), str(len(point_array_super)) + ' Songs')
                print('Durchschnittliche Punktzahl der good Songs: ' +
                    str(np.mean(point_array_good)), str(len(point_array_good)) + ' Songs')
                print('Durchschnittliche Punktzahl der medium Songs: ' +
                    str(np.mean(point_array_medium)), str(len(point_array_medium)) + ' Songs')
                print('Durchschnittliche Punktzahl der bad Songs: ' +
                    str(np.mean(point_array_bad)), str(len(point_array_bad)) + ' Songs')


def build_song_dict(song_dict):
    ret_dict = {}
    for key in song_dict:
        song_id = song_dict[key]['id']
        ret_dict[song_id] = {}
        for par in song_dict[key]:
            ret_dict[song_id][par] = song_dict[key][par]
        ret_dict[song_id]['points'] = 0
    return ret_dict


def get_listening_ids(listened_songs):
    entered_ids = []
    test_ids_bad = []
    test_ids_medium = []
    test_ids_good = []
    test_ids_super = []
    for key in listened_songs:
        max_amount_entered = min(5, len(listened_songs[key]['super']))
        if max_amount_entered > 1:
            amount_entered = random.randint(1, max_amount_entered)
        else:
            amount_entered = 1
        rnd_entered_indices = get_random_song_indices(
            listened_songs[key]['super'], amount_entered)
        ent = [listened_songs[key]['super'][index]
               for index in rnd_entered_indices]
        entered_ids.append(ent)
        listened_songs[key]['super'] = [
            song_id for song_id in listened_songs[key]['super'] if song_id not in ent]
        for like, test_id_list in zip(['bad', 'medium', 'good', 'super'], [test_ids_bad, test_ids_medium, test_ids_good, test_ids_super]):
            test_id_max_amount = len(listened_songs[key][like])
            if test_id_max_amount > 0:
                test_id_amount = random.randint(1, test_id_max_amount)
            else:
                test_id_amount = 0
            rnd_test_indices = get_random_song_indices(
                listened_songs[key][like], test_id_amount)
            test_id_list.append([listened_songs[key][like][index]
                                 for index in rnd_test_indices])
    return entered_ids, test_ids_bad, test_ids_medium, test_ids_good, test_ids_super


def get_random_song_indices(id_list, amount):
    if len(id_list) > 0:
        return random.sample(range(0, len(id_list)), amount)
    else:
        return []
