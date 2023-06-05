import os

from flask import Flask, jsonify, redirect, url_for

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(os.getenv('INSTANCE_PATH'))
    except OSError:
        pass

    # a simple page that says hello
    #@app.route('/')
    #def hello():
    #    return 'Hello, World!'

    # importing database
    from . import db
    db.init_app(app)
    
    # importing auth blueprint
    from . import auth
    app.register_blueprint(auth.bp)
    
    # importing movies blueprint
    from . import movies
    app.register_blueprint(movies.bp)
    app.add_url_rule('/', endpoint='movies.index')

    return app