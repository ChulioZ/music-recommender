from flask import Flask, jsonify
import time
import datetime
from db_creator import build_db, change_db
from recommender import recommend, test_recommend
from kmeans_tester import test_kmeans
from listening_count_reader import get_listened_songs

app = Flask(__name__)


@app.route('/', methods=['GET'])
def m():
    start = time.time()
    # build_db()  # if the data base has to be built from scrath
    # change_db() # if changes to the data base have to be made
    for i in range(0, 20):
        listened_songs, limits = get_listened_songs()
        test_kmeans(listened_songs, limits)
    print(str(datetime.timedelta(seconds=time.time()-start)))
    return 'Test'


if __name__ == "__main__":
    app.run(host="0.0.0.0", threaded=True)
