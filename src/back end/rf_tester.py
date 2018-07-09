import itertools
import random

import numpy as np
from sklearn.ensemble import RandomForestClassifier

from constants import PARS, RF_TEST_FILE_PATH
from listening_count_reader import get_listened_songs
from song_dict_reader import get_rnd_good_songs, read_song_dict_w_labels


def test_rf():
    ''' Tests different Random Forest configurations. '''
    song_dict = read_song_dict_w_labels()
    results = {}
    with open(RF_TEST_FILE_PATH, 'w') as outfile:
        for i in range(1, 20):  # test 20 different random limits
            ent_amount = random.randint(1, 5)  # 1-5 songs as entered songs
            limits = get_rnd_limits()
            entered_ids = get_rnd_good_songs(
                song_dict, ent_amount, limits=limits)
            # all users and the songs they've listened to
            listened_songs = get_listened_songs(limits=limits)[0]
            # get all combinations of PARS containing 3-6 parameters
            par_combinations = []
            for i in range(3, len(PARS) + 1):
                listing = [list(x) for x in itertools.combinations(PARS, i)]
                par_combinations.extend(listing)
            # test for each combination
            for par_combination in par_combinations:
                # lists for building the Random Forest
                rf_pars = []
                rf_targets = []
                rf_ids = []  # tracks the songs that are already included
                rf_targets_quant = []  # tracks how often each song is already included
                for user in listened_songs.keys():
                    # only users are taken into account to build the random forest that
                    # have at least one of the entered songs in their 'good' category
                    contains_good_song = False
                    for song_id in entered_ids:
                        contains_good_song = song_id in listened_songs[user]['good']
                    if contains_good_song:
                        for like, like_value in zip(['bad', 'medium', 'good'], [1, 2, 3]):
                            for song_id in listened_songs[user][like]:
                                if song_id not in rf_ids:
                                    rf_ids.append(song_id)
                                    rf_pars.append([song_dict[song_id][par]
                                                    for par in par_combination])
                                    rf_targets_quant.append(1)
                                    rf_targets.append(like_value)
                                # if a value already exists for that song, take the
                                # average of all values
                                else:
                                    index = rf_ids.index(song_id)
                                    rf_targets_quant[index] += 1
                                    rf_targets[index] = (rf_targets[index] + like_value) \
                                        / rf_targets_quant[index]
                # convert integers back to bad, medium, and good category strings
                for index in range(0, len(rf_targets)):
                    if int(rf_targets[index]) == 1:
                        rf_targets[index] = 'bad'
                    elif int(rf_targets[index]) == 2:
                        rf_targets[index] = 'medium'
                    else:
                        rf_targets[index] = 'good'
                scores = []
                for j in range(0, 3):  # build the RF 3 times and take the average score
                    # split into training and test data 70/30
                    training_indices = random.sample(
                        range(0, len(rf_targets)), int(0.7 * len(rf_targets)))
                    test_indices = [index for index in range(0, len(rf_targets))
                                    if user not in training_indices]
                    rf_targets_train = [rf_targets[index]
                                        for index in training_indices]
                    rf_targets_test = [rf_targets[index]
                                       for index in test_indices]
                    rf_pars_train = [rf_pars[index]
                                     for index in training_indices]
                    rf_pars_test = [rf_pars[index] for index in test_indices]
                    # build the Random Forest
                    rf = RandomForestClassifier()
                    rf.fit(rf_pars_train, rf_targets_train)
                    scores.append(rf.score(rf_pars_test, rf_targets_test))
                outfile.write(
                    'Limits: [' + str(limits[0]) + ', ' + str(limits[1]) + ']   ')
                outfile.write('Songs entered: ' + str(ent_amount) + '   ')
                par_comb_string = ''
                for i in range(0, len(par_combination) - 1):
                    par_comb_string += par_combination[i] + ', '
                par_comb_string += par_combination[len(par_combination) - 1]
                outfile.write('Par-combination: [' + par_comb_string + ']   ')
                avg_score = np.mean(scores)
                outfile.write('Average score: ' + str(avg_score) + '\n')
                for arg in [limits, ent_amount, par_combination]:
                    if str(arg) not in results.keys():
                        results[str(arg)] = []
                    results[str(arg)].append(avg_score)
        for key in results.keys():
            outfile.write('Average score for ' + key + ': ' + str(np.mean(results[key])) + '\n')


def get_rnd_limits():
    ''' Get random limits for bad, medium, and good categories. '''
    limit_a = random.randint(2, 10)
    limit_b = max(random.randint(10, 30), limit_a + 5)
    return [limit_a, limit_b]