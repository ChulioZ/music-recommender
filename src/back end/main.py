import random

from flask import Flask, jsonify, request

from constants import WELCOMESTRING
from listening_count_reader import get_listened_songs
from recommender import recommend, recommend_w_rf
from song_dict_reader import (get_rnd_entered_songs, get_rnd_good_songs,
                              read_song_dict_w_labels, search_songs)

app = Flask(__name__)


@app.route('/')
def welcome():
    '''Welcome page with instructions on how to use the MRS.'''
    return WELCOMESTRING


@app.route('/mrs', methods=['GET'])
def make_recommendation(random_forest=False,
                        rec_amount=10,
                        entered_songs=None,
                        entered_amount=1):
    '''
    Main function that's called when a user enters the page. Prints a
    recommendation of rec_amount songs for the entered songs.

    random_forest: If False (default), recommendation is done via
    kmeans++ clustering. If True, it's done via random forest.

    rec_amount: The amount of songs to recommend.

    entered_songs: List of song ids the user has entered. If none is
    provided, a random list will be created. Note that if you want to
    use random forest, only enter song ids that at least one user has
    in his good category.

    entered_amount: the amount of songs the randomly created list of
    entered songs shall contain. Only relevant if no list of entered
    songs is provided.
    '''
    req_rf = request.args.get('rf')
    if req_rf == 'True' or req_rf == 'true':
        random_forest = True
    req_ra = request.args.get('recamount')
    if req_ra is not None:
        rec_amount = int(req_ra)
    req_ea = request.args.get('entamount')
    if req_ea is not None:
        entered_amount = int(req_ea)
    if request.args.get('ent1') is not None:
        entered_songs = build_entered_list(request)
    song_dict = read_song_dict_w_labels()
    if random_forest:
        if entered_songs is None:
            entered_songs = get_rnd_good_songs(song_dict, entered_amount)
        return recommend_w_rf(song_dict, entered_songs, rec_amount)
    else:
        if entered_songs is None:
            entered_songs = get_rnd_entered_songs(song_dict, entered_amount)
        return recommend(song_dict, entered_songs, rec_amount)


@app.route('/songs', methods=['GET'])
def list_songs():
    '''Lists all songs that meet the search criteria.'''
    artist = request.args.get('artist')
    title = request.args.get('title')
    song_id = request.args.get('id')
    eligibility = request.args.get('elig')
    return jsonify(search_songs(artist, title, song_id, eligibility))


def build_entered_list(request):
    ''' Build the list of entered songs from the URL input. '''
    entered_list = []
    i = 1
    while i:
        ent = 'ent{}'.format(i)
        ent_input = request.args.get(ent)
        if ent_input is not None:
            entered_list.append(ent_input)
            i += 1
        else:
            i = False
    return entered_list


if __name__ == "__main__":
    # Start the Flask server
    app.run(host="0.0.0.0", threaded=True)
