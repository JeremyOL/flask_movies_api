import functools

from flask import (
    Blueprint, g, redirect, request, session, jsonify, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from movies_api.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    db = get_db()
    error = None

    if not username:
        error = 'Username is required.'
    if not password:
        error = 'Password is required.'
    
    if error is None:
        try:
            db.execute('INSERT INTO user (username, password) VALUES (?, ?)', (username, generate_password_hash(password)))
            db.commit()
        except db.IntegrityError:
            error = f"User {username} is already registered."
        else:
            return jsonify({
                'status': 'ok', 
                'message': 'user created'
            })
    
    return jsonify({
        'status': 'bad',
        'message': error
    })

@bp.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    db = get_db()
    error = None
    user = None
    if username is None:
        error = 'Username required'
    elif password is None:
        error = 'Password required'
    else:
        user = db.execute('SELECT * FROM user WHERE username = ?', (username,)).fetchone()
        if user is None:
            error = 'Incorrect username'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password'
        
    if error is None:
        session.clear()
        session['user_id'] = user['id']
        return jsonify({
            'status' : 'ok',
            'message' : 'login success',
            'user_id' : user['id']
        })
    
    return jsonify({
        'status': 'bad',
        'message': error
    })

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view