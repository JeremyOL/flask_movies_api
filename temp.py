api_v1 = '/movies_api/v1/'

@app.route('/')
def index():
    return redirect(url_for('hello'))

@app.route(api_v1)
def hello():
    return jsonify({'result' : 'api on'})

@app.route(api_v1 + 'movies')
def getMovies():
    return jsonify({'result' : 'ok'})

