import json
import random

from constants import MSD_DATA_FILE_PATH, MSD_DATA_LABELED_PART_FILE_PATH, PARS
from listening_count_reader import get_listened_songs


def read_song_dict_wo_labels():
    '''
    Read the data for all the songs without labels attached to it.

    This was only needed while developing the app and is not used by
    the recommender system as the data is now labeled by kmeans++ and
    thus stored in different files. Note that this method is not even
    callable as the unlabeled data file is not part of the git repo.
    The method is just here as a reference.
    '''
    with open(MSD_DATA_FILE_PATH, 'r') as f:
        song_dict = json.load(f)
    return song_dict


def read_song_dict_w_labels():
    ''' Read the data for all the songs from the json files. '''
    song_dict = {}
    for i in range(1, 8):
        with open(MSD_DATA_LABELED_PART_FILE_PATH.format(i), 'r') as f:
            temp_song_dict = json.load(f)
            song_dict = {**song_dict, **temp_song_dict}
            f.close()
    return song_dict


def build_song_list(artist, title, song_id, eligibility):
    '''
    Builds a list of songs meeting specific search criteria to display
    on /songs.

    artist: artist of the song

    title: title of the song

    song_id: id of the song

    eligibility: True if the song shall be eligible to enter for Random
    Forest recommendation, False otherwise
    '''
    song_dict = read_song_dict_w_labels()
    songs_to_pop = []
    # remove all songs that don't match all the search criteria
    for song in song_dict:
        if artist is not None and \
                song_dict[song]['artist'].lower() != artist.lower():
            songs_to_pop.append(song)
            continue
        if title is not None and \
                song_dict[song]['title'].lower() != title.lower():
            songs_to_pop.append(song)
            continue
        if song_id is not None and \
                song_dict[song]['id'].lower() != song_id.lower():
            songs_to_pop.append(song)
            continue
        if eligibility is not None and \
                str(song_dict[song]['rf_enterable']).lower() != \
                eligibility.lower():
            songs_to_pop.append(song)
            continue
        # remove all information that's irrelevant for the user
        for key in PARS + ['points', 'label']:
            song_dict[song].pop(key)
    for song in songs_to_pop:
        song_dict.pop(song)
    return song_dict


def get_rnd_entered_songs(song_dict, amount):
    ''' Get an amount of random song ids. '''
    return random.sample(song_dict.keys(), amount)


def get_rnd_good_songs(song_dict, amount):
    '''
    Get an amount of random song ids that at least one user has in his
    good category.
    '''
    listened_songs = get_listened_songs(limits=[9, 24])[0]
    # find all songs that at least one user has in his good category
    good_songs = []
    for user in listened_songs.keys():
        good_songs.extend(listened_songs[user]['good'])
    song_ids_2_pop = []
    song_dict_temp = song_dict.copy()
    for song_id in song_dict_temp:
        if song_id not in good_songs:
            song_ids_2_pop.append(song_id)
    # remove all songs that aren't good
    for song_id in song_ids_2_pop:
        song_dict_temp.pop(song_id)
    return random.sample(song_dict_temp.keys(), amount)
