import os

from flask import Flask
from . import db
from . import auth
from . import characters


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'gamr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Initialize our database / db functions
    db.init_app(app)

    # Register our auth blueprint
    app.register_blueprint(auth.bp)

    # Register the character blueprint
    app.register_blueprint(characters.bp)

    app.add_url_rule('/', endpoint='character_index')

    return app
