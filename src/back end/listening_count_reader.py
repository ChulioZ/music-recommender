import random
from os.path import dirname, abspath


def get_listening_ids():
    file_path = dirname(dirname(dirname(abspath(__file__))))
    file_path_good = file_path+"\\user_song_listen_numbers_reduced.txt"
    file_path_bad = file_path+"\\user_song_listen_numbers_ones.txt"
    file_good = open(file_path_good, "r")
    file_bad = open(file_path_bad, "r")
    listened_songs = {}
    for line in file_good:
        user_id, song_id, cnt = line.split('\t')
        if user_id not in listened_songs:
            listened_songs[user_id] = {}
            listened_songs[user_id]['good'] = []
            listened_songs[user_id]['bad'] = []
        listened_songs[user_id]['good'].append(song_id)
    for line in file_bad:
        user_id, song_id, cnt = line.split('\t')
        if user_id in listened_songs and len(listened_songs[user_id]['good']) > 9:
            listened_songs[user_id]['bad'].append(song_id)
    entered_ids = []
    test_ids_good = []
    test_ids_bad = []
    for user_id in listened_songs:
        if len(listened_songs[user_id]['good']) > 9:
            random.shuffle(listened_songs[user_id]['good'])
            factor = random.uniform(0.1, 0.9)
            train_number = int(factor * len(listened_songs[user_id]['good']))
            ent_array = []
            test_array = []
            for i in range(0, len(listened_songs[user_id]['good'])):
                if i <= train_number:
                    ent_array.append(listened_songs[user_id]['good'][i])
                else:
                    test_array.append(listened_songs[user_id]['good'][i])
            entered_ids.append(ent_array)
            test_ids_good.append(test_array)
            test_ids_bad.append(listened_songs[user_id]['bad'])

    return entered_ids, test_ids_good, test_ids_bad
