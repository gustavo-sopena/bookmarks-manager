# author: Gustavo Sopena
# date started: 2024-08-10 at 1530

import os
from flask import Flask, render_template

def create_app(test_config=None) -> Flask:
    '''This function will create the Flask application.'''

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'bookmarks_manager.sqlite')
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from bookmarks_manager import db
    db.register_database(app)

    @app.route('/', methods=['GET'])
    def index() -> str:
        '''This function is the index page of the website.'''

        return render_template('base.html')

    return app
