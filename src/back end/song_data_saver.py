import glob
import json
import math
import os
from os.path import abspath, dirname

import numpy as np

import hdf5_getters as GETTERS
from constants import (FILE_PATH, INITIAL_OUTPUT_FILE_PATH, METHODS,
                       MSD_DATA_PATH)
from mice import MICE


def save_songs():
    '''
    Reads the song infos for all songs in the directory specified in
    MSD_DATA_PATH, imputes missing data, normalizes the data and stores it as
    a JSON file.
    '''
    # read all relevant infos from the songs and store them in a dictionary
    print('Reading song infos from the h5 files ...')
    song_dict = {}
    i = -1
    ids = set()
    pars = ['loudness', 'hotttnesss', 'tempo', 'timeSig', 'songkey', 'mode']
    for root, dirs, files in os.walk(MSD_DATA_PATH):
        files = glob.glob(os.path.join(root, '*'+'.h5'))
        for file in files:
            h5 = GETTERS.open_h5_file_read(file)
            id = GETTERS.get_song_id(h5).decode('UTF-8')
            # if there are multiple song files with the same id only the first
            # is saved
            if id not in ids:
                i += 1
                ids.add(id)
                song_dict[i] = {}
                song_dict[i]['id'] = id  # save the song id
                song_dict[i]['title'] = GETTERS.get_title(
                    h5).decode('UTF-8').replace("'", "")  # save the title
                song_dict[i]['artist'] = GETTERS.get_artist_name(
                    h5).decode('UTF-8').replace("'", "")  # save the artist

                # save the remaining parameters or, whenever a value is
                # missing, save np.NaN instead
                for key, method in zip(pars, METHODS):
                    value = getattr(GETTERS, method)(h5)
                    if math.isnan(value):
                        song_dict[i][key] = np.NaN
                    else:
                        song_dict[i][key] = value
                h5.close()

    # impute missing values via fancyimpute MICE imputation and store the new
    # values in the dictionary
    print('Building the array for MICE ...')
    song_array = []
    for index in range(0, len(song_dict)):
        song_array.append([song_dict[index][par] for par in pars])

    print('MICE ...')
    mc = MICE()
    a = mc.complete(np.array(song_array))

    print('Storing imputed data in song dictionary ...')
    # store the values for each parameter in a list for the normalization
    # in the next step
    val_lists = []
    for par in pars:
        val_lists.append([])

    for index in range(0, len(song_dict)):
        for par, val_list, nr in zip(pars, val_lists, range(0, len(pars))):
            value = a[index, nr]
            song_dict[index][par] = value
            val_list.append(value)

    # normalize the values
    print('Normalizing the values ...')
    for par, val_list in zip(pars, val_lists):
        max_value = -float("inf")
        min_value = float("inf")
        for index in song_dict:
            max_value = max(max_value, song_dict[index][par])
            min_value = min(min_value, song_dict[index][par])
        for index in song_dict:
            song_dict[index][par] = (
                song_dict[index][par] - np.mean(val_list)) / (max_value - min_value) * 100

    # save the data as a JSON file
    print('Saving JSON ...')
    with open(INITIAL_OUTPUT_FILE_PATH, 'w') as outfile:
        json.dump(song_dict, outfile)

    print('done')
