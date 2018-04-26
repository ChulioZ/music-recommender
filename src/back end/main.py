from flask import Flask, jsonify
import msd_walker

app = Flask(__name__)


@app.route('/', methods=['GET'])
def recommend():
    msd_walker.read_song_infos()
    return msd_walker.test()


if __name__ == "__main__":
    app.run(host="0.0.0.0", threaded=True)
