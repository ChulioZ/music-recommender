from flask import Flask, jsonify
from db_creator import read_song_infos
from clustering import do_kmeans
from recommender import recommend

app = Flask(__name__)


@app.route('/', methods=['GET'])
def m():
    # read_song_infos()
    # do_kmeans()
    ret_dict = recommend(['SOMAKIT12A58A7E292', 'SOPSAIO12A58A7AE45'])
    print(ret_dict['SOHXDYZ12A8C145925']['points'],
          ret_dict['SOYRSUR12A6D4FB19B']['points'])
    return 'Test'


if __name__ == "__main__":
    app.run(host="0.0.0.0", threaded=True)
