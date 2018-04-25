import json
from flask import Flask

app = Flask(__name__)


@app.route('/', methods=['GET'])
def recommend():
    return 'Test'


if __name__ == "__main__":
    app.run(host="0.0.0.0", threaded=True)
