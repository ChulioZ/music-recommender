from os.path import dirname, abspath
import json
from itertools import islice


file_path = dirname(dirname(dirname(abspath(__file__))))


def read_song_dict_wo_labels():
    with open(file_path + '/msd_data.txt', 'r') as f:
        song_dict = json.load(f)
    return build_song_dict(song_dict)


def read_song_dict_w_labels():
    song_dict = {}
    for i in range(1, 8):
        with open(file_path + '/msd_data_labeled' + str(i) + '.txt', 'r') as f:
            temp_song_dict = json.load(f)
            song_dict = {**song_dict, **temp_song_dict}
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


def change():
    with open(file_path + '/msd_data_labeled.txt', 'r') as f:
        song_dict = json.load(f)
    i = 1
    for part in chunks(song_dict):
        print(len(part))
        with open(file_path + '/msd_data_labeled' + str(i) + '.txt', 'w') as f:
            json.dump(part, f)
        i += 1


def chunks(song_dict):
    it = iter(song_dict)
    for i in range(0, len(song_dict), 150000):
        yield {song:song_dict[song] for song in islice(it, 150000)}