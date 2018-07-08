import random

from constants import USER_SONG_LISTEN_NUMBERS_FILE_PATH


def get_listened_songs(limits=None, needs_good=False):
    '''
    Reads all data regarding users and the songs they've listened to
    from the file. Returns a dictionary containing the users and their
    songs split into bad, medium, and good categories; and returns the
    limits between those categories.

    limits: List of limits between bad, medium, and good categories. If
    limits is None, random limits will be chosen.

    needs_good: specifies if only users shall be kept in the dictionary
    that have at least one song in the good category.
    '''
    listen_file = open(USER_SONG_LISTEN_NUMBERS_FILE_PATH, "r")
    if limits is None:  # choose random limits
        limit_a = random.randint(2, 10)
        limit_b = max(random.randint(10, 25), limit_a + 3)
        limits = [limit_a, limit_b]
    else:
        limit_a, limit_b = limits
    listened_songs = {}
    for line in listen_file:
        user_id, song_id, cnt = line.split('\t')
        if user_id not in listened_songs:
            listened_songs[user_id] = {}
            listened_songs[user_id]['bad'] = []
            listened_songs[user_id]['medium'] = []
            listened_songs[user_id]['good'] = []
        count = int(cnt)  # how often the user heard the song
        if count < limit_a:  # bad song
            listened_songs[user_id]['bad'].append(song_id)
        elif count < limit_b:  # medium song
            listened_songs[user_id]['medium'].append(song_id)
        else:  # good song
            listened_songs[user_id]['good'].append(song_id)
    if needs_good:
        # remove all users that don't have at least one good song
        users_to_remove = []
        for user in listened_songs:
            if len(listened_songs[user]['good']) < 1:
                users_to_remove.append(user)
        for user in users_to_remove:
            listened_songs.pop(user)
    return listened_songs, limits


def get_random_test_listeners(limits):
    '''
    For each user, randomly chooses some of the songs they've listened
    to as bad, medium, and good test songs and some of the good ones as
    songs they provide as input for the recommender system.

    This was needed for testing purposes while developing and is not
    used for the recommender system itself.

    limits: List containing to int numbers to act as limits between the
    bad, medium, and good categories
    '''
    entered_ids = []
    test_ids_bad = []
    test_ids_medium = []
    test_ids_good = []
    # we need users that have at least one good song to choose one or more of
    # them to act as input for the recommender system
    listened_songs = get_listened_songs(limits=limits, needs_good=True)
    for user in listened_songs:
        # choose at least one, at most five of the good songs as input songs
        max_amount_entered = min(5, len(listened_songs[user]['good']))
        if max_amount_entered > 1:
            amount_entered = random.randint(1, max_amount_entered)
        else:
            amount_entered = 1
        rnd_entered_indices = get_random_indices(
            listened_songs[user]['good'], amount_entered)
        ent = [listened_songs[user]['good'][index]
               for index in rnd_entered_indices]
        entered_ids.append(ent)
        # For the bad, medium, and the remaining good songs, choose a random
        # amount of them to act as test songs
        listened_songs[user]['good'] = [song_id for song_id in
                                        listened_songs[user]['good']
                                        if song_id not in ent]
        for like, test_id_list in zip(['bad', 'medium', 'good'],
                                      [test_ids_bad, test_ids_medium,
                                       test_ids_good]):
            test_id_max_amount = len(listened_songs[user][like])
            if test_id_max_amount > 0:
                test_id_amount = random.randint(1, test_id_max_amount)
            else:
                test_id_amount = 0
            rnd_test_indices = get_random_indices(
                listened_songs[user][like], test_id_amount)
            test_id_list.append([listened_songs[user][like][index]
                                 for index in rnd_test_indices])
    return entered_ids, test_ids_bad, test_ids_medium, test_ids_good


def get_random_indices(id_list, amount):
    ''' Get a list of amount random indices of a specified list'''
    if len(id_list) > 0:
        return random.sample(range(0, len(id_list)), amount)
    else:
        return []
