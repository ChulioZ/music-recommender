from flask import Flask, jsonify
from db_creator import read_song_infos
from clustering import do_kmeans
from recommender import recommend, test_recommend

app = Flask(__name__)


@app.route('/', methods=['GET'])
def m():
    # read_song_infos()
    # do_kmeans()
    #ret_dict = recommend(['SOMAKIT12A58A7E292', 'SOPSAIO12A58A7AE45'])
    #print(ret_dict)
    #ret_dict2 = test_recommend(['SOMAKIT12A58A7E292', 'SOPSAIO12A58A7AE45'], ['SOHXDYZ12A8C145925', 'SOYRSUR12A6D4FB19B'])
    #print(ret_dict2['SOHXDYZ12A8C145925'], ret_dict2['SOYRSUR12A6D4FB19B'])
    return 'Test'


if __name__ == "__main__":
    app.run(host="0.0.0.0", threaded=True)
