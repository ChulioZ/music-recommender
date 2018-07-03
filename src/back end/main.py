from flask import Flask, jsonify
import time
import datetime
from db_creator import build_db, change_db
from recommender import recommend, test_recommend
from kmeans_tester import test_kmeans, add_kmeans_labels, read_song_dict_w_labels
from listening_count_reader import get_listened_songs
import random

app = Flask(__name__)


@app.route('/', methods=['GET'])
def m():
    start = time.time()
    # build_db()  # if the data base has to be built from scrath
    # change_db()  # if changes to the data base have to be made
    # to test different k-means++-clusterings
    # for i in range(0, 20):
    #     listened_songs, limits = get_listened_songs()
    #     test_kmeans(listened_songs, limits)
    add_kmeans_labels()  # to add the clustering labels for each song
    # song_dict = read_song_dict_w_labels()
    # rnd_entered_songs = random.sample(song_dict.keys(), random.randint(1,5))
    # recommend(rnd_entered_songs)
    print(str(datetime.timedelta(seconds=time.time()-start)))
    return 'Test'


if __name__ == "__main__":
    app.run(host="0.0.0.0", threaded=True)
