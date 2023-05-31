from flask import Flask, jsonify

app = Flask(__name__)

api_v1 = '/movies_api/v1/'

@app.route(api_v1 + 'movies')
def getMovies():
    return jsonify({'result' : 'ok'})

if __name__ == '__main__':
    app.run(debug=True, port=4000)