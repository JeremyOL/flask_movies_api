from flask import (
    Blueprint, request, jsonify, g
)

import json
import datetime

from movies_api.db import get_db
from movies_api.auth import login_required

bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route('/save_movie', methods=['POST'])
@login_required
def save_movie():
    data = request.json
    user_id = g.user['id']
    movie_id = data.get('movie_id')
    created = datetime.datetime.now()

    db = get_db()
    error = None
    
    if user_id is None:
        error = "User required"
    elif movie_id is None:
        error = "Movie required"
    else:
        favorite_exists = db.execute("SELECT * FROM user_movies WHERE user_id = ? and movie_id = ?",(user_id, movie_id)).fetchone()
        if favorite_exists is None:
            try:
                db.execute("INSERT INTO user_movies (user_id, created, movie_id) VALUES (?, ?, ?)", (user_id, created, movie_id))
                db.commit()
            except:
                error = 'Error ???'
            else:
                return jsonify({
                    'status': 'ok',
                    'message': 'Movie saved'
                })
        else:
            error = "Movie already saved"
    return jsonify({
        'status': 'bad',
        'message': error
    })
        
    