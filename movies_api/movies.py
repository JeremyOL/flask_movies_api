from flask import(
    Blueprint, g, request, jsonify
)

import requests
import os
import json

from movies_api.db import get_db
#from movies_api.auth import login_required

bp = Blueprint('movies', __name__, url_prefix='/movies')

MOVIES_API_KEY = os.getenv('MOVIES_API_KEY')
MOVIES_API_URL = os.getenv('MOVIES_API_URL')

@bp.route('/')
def index():
    db = get_db()
    movies = db.execute(
        'SELECT fm.id, fm.user_id, fm.created, fm.imdb_movie_id'
        ' FROM favorite_movies fm JOIN user u ON fm.user_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return jsonify({
        'status': 'ok',
        'message': 'index loaded',
        'movies': movies
    })
    
@bp.route('/search_by_name', methods=['GET'])
def search_movies_by_name():
    """
        Request a movie using the following URL:
            https://api.themoviedb.org/3/search/movie
        Query Params:
            name: name of the movie
            lang: languaje of the response, default es-MX
            page: page of the response
        Returns:
            List of movies containing the searched name
    """
    name = request.args.get('name', '')
    lang = request.args.get('lang', 'es-MX')
    page = request.args.get('page', '1')
    url = '{0}/search/movie?query={1}&language={2}&page={3}&api_key={4}'.format(MOVIES_API_URL, name, lang, page , MOVIES_API_KEY)
    response = requests.get(url)
    return jsonify({
        'status': 'ok', 
        'message': 'Movies by name',
        'movies': json.loads(response.text)
    })
    
@bp.route('/<movie_id>/details', methods=['GET'])
def movie_details(movie_id):
    """
        Request movie details using the following URL:
            https://api.themoviedb.org/3/movie/{movie_id}
        Arguments:
            movie_id: id of the movie
        Query Params:
            lang: languaje of the response, default es-MX
    """
    lang = request.args.get('lang', 'es-MX')
    url = '{0}/movie/{1}?language={2}&api_key={3}'.format(MOVIES_API_URL, movie_id, lang, MOVIES_API_KEY)
    response = requests.get(url)
    return jsonify({
        'status': 'ok', 
        'message': 'Movie details',
        'movie': json.loads(response.text)
    })