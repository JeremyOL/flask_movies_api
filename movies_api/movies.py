from flask import(
    Blueprint, g, request, jsonify
)

import requests
import os
import json

from movies_api.db import get_db
from movies_api.auth import login_required

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
            List of movies containing the searched name as movies
    """
    name = request.args.get('name', '')
    lang = request.args.get('lang', 'es-MX')
    page = request.args.get('page', '1')
    url = f'{MOVIES_API_URL}/search/movie?query={name}&language={lang}&page={page}&api_key={MOVIES_API_KEY}'
    response = requests.get(url)
    return jsonify({
        'status': 'ok', 
        'message': 'Movies by name',
        'movies': json.loads(response.text)
    })
    
@bp.route('/<movie_id>/details', methods=['GET'])
def single_movie_details(movie_id):
    """
        Request movie details using the following URL:
            https://api.themoviedb.org/3/movie/{movie_id}
        Arguments:
            movie_id: id of the movie
        Query Params:
            lang: languaje of the response, default es-MX
        Returns:
            Detailed information of the movie as movie
    """
    lang = request.args.get('lang', 'es-MX')
    url = _tmdb_movie_details(movie_id, lang)
    response = requests.get(url)
    return jsonify({
        'status': 'ok', 
        'message': 'Movie details',
        'movie': json.loads(response.text)
    })
    
@bp.route('/list_details', methods=['GET'])
def list_movies_details():
    """
        Request movie details from list of ids
        Body:
            json format list of movies ids
            ex. {
                movie_ids:[808,807,806]
            }
        Query Params:
            lang: languaje of the response, default es-MX
        Return:
            id, title and tagline of the movies as movies_details.
    """
    data = request.json
    movie_ids = data.get('movie_ids')
    lang = request.args.get('lang', 'es-MX')
    error = None
    
    if not movie_ids:
        error = 'movie_ids not found'
    
    if not error:
        movies_details = []
        for movie_id in movie_ids:
            url = _tmdb_movie_details(movie_id, lang)
            response = requests.get(url)
            response_data = json.loads(response.text)
            if response_data.get('status_code'):
                continue
            movies_details.append({
                'id': response_data.get('id'),
                'title': response_data.get('title'),
                'tagline': response_data.get('tagline')
            })
        return jsonify({
            'status':'ok',
            'message': 'Movies details',
            'movies_details': movies_details
        })
            
    return jsonify({
        'status': 'bad',
        'message': error
    })
    
def _tmdb_movie_details(movie_id, lang):
    return f'{MOVIES_API_URL}/movie/{movie_id}?language={lang}&api_key={MOVIES_API_KEY}'