from listening_count_reader import get_listened_songs
from recommender import recommend_w_rf
from song_dict_reader import read_song_dict_w_labels
import random
import numpy as np
from constants import LIMIT_LIST


def control_quality_rf():
    ''' Controls the quality of the RF recommendations. '''
    listened_songs = get_listened_songs(limits=LIMIT_LIST, needs_good=True)[0]
    users_to_remove = random.sample(
        listened_songs.keys(), len(listened_songs) - 250)
    for user in users_to_remove:
        listened_songs.pop(user)
    song_dict = read_song_dict_w_labels()
    bad_points = []
    medium_points = []
    good_points = []
    i = 1
    for user in listened_songs:
        entered_ids = random.sample(
            listened_songs[user]['good'],
            min(random.randint(1, 3), len(listened_songs[user]['good'])))
        point_dict = recommend_w_rf(song_dict, entered_ids, 1)[1]
        for like, point_list in zip(['bad', 'medium', 'good'],
                                    [bad_points, medium_points, good_points]):
            songs_to_check = [
                song_id for song_id in listened_songs[user][like]
                if song_id not in entered_ids]
            for song_id in songs_to_check:
                point_list.append(point_dict[song_id])
        print(i, '/', len(listened_songs))
        i += 1
        for song in song_dict:
            song_dict[song]['points'] = 0
    print('average points for bad songs', np.mean(bad_points))
    print('average points for medium songs', np.mean(medium_points))
    print('average points for good songs', np.mean(good_points))
