import random
from os.path import dirname, abspath


def get_listened_songs():
    file_path = dirname(dirname(dirname(abspath(__file__))))
    file_path_listen_numbrers = file_path+"\\user_song_listen_numbers.txt"
    listen_file = open(file_path_listen_numbrers, "r")
    limit_a = random.randint(2,6)
    limit_b = max(random.randint(5, 15), limit_a + 3)
    limit_c = max(random.randint(10, 25), limit_b + 5)
    limits = [limit_a, limit_b, limit_c]
    listened_songs = {}
    for line in listen_file:
        user_id, song_id, cnt = line.split('\t')
        if user_id not in listened_songs:
            listened_songs[user_id] = {}
            listened_songs[user_id]['good'] = []
            listened_songs[user_id]['bad'] = []
            listened_songs[user_id]['medium'] = []
            listened_songs[user_id]['super'] = []
        count = int(cnt)
        if count < limit_a:
            listened_songs[user_id]['bad'].append(song_id)
        elif count < limit_b:
            listened_songs[user_id]['medium'].append(song_id)
        elif count < limit_c:
            listened_songs[user_id]['good'].append(song_id)
        else:
            listened_songs[user_id]['super'].append(song_id)
    keys2remove = []
    for key in listened_songs:
        if len(listened_songs[key]['super']) < 1:
            keys2remove.append(key)
    for key in keys2remove:
        listened_songs.pop(key)

    return listened_songs, limits
