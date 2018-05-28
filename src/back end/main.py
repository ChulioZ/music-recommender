from flask import Flask, jsonify
from db_creator import read_song_infos
from clustering import do_kmeans

app = Flask(__name__)


@app.route('/', methods=['GET'])
def recommend():
    # This method call shouldn't be needed any longer -- the data base is complete!
    # read_song_infos()
    do_kmeans()
    return 'Test'


if __name__ == "__main__":
    app.run(host="0.0.0.0", threaded=True)
