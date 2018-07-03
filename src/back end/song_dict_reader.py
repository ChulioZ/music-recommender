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


def build_song_dict(song_dict):
    ret_dict = {}
    for key in song_dict:
        song_id = song_dict[key]['id']
        ret_dict[song_id] = {}
        for par in song_dict[key]:
            ret_dict[song_id][par] = song_dict[key][par]
        ret_dict[song_id]['points'] = 0
    return ret_dict