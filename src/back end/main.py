from flask import Flask, jsonify
import time
import datetime
from db_creator import build_db, change_db
from recommender import recommend, test_recommend
from kmeans_tester import test_kmeans
from listening_count_reader import get_listening_ids

app = Flask(__name__)


@app.route('/', methods=['GET'])
def m():
    start = time.time()
    # build_db()  # if the data base has to be built from scrath
    # change_db() # if changes to the data base have to be made
    entered_ids, test_ids_good, test_ids_bad = get_listening_ids()
    test_kmeans(entered_ids, test_ids_good, test_ids_bad)
    print(str(datetime.timedelta(seconds=time.time()-start)))
    return 'Test'


if __name__ == "__main__":
    app.run(host="0.0.0.0", threaded=True)
