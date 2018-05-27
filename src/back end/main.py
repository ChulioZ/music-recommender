from flask import Flask, jsonify
import msd_walker

app = Flask(__name__)


@app.route('/', methods=['GET'])
def recommend():
    # This method call shouldn't be needed any longer -- the data base is complete!
    # msd_walker.read_song_infos()
    return 'Test'


if __name__ == "__main__":
    app.run(host="0.0.0.0", threaded=True)
