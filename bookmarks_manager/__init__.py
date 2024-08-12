# author: Gustavo Sopena
# date started: 2024-08-10 at 1530

import os
from datetime import datetime
from flask import Flask, render_template, request

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

    @app.route('/', methods=['GET', 'POST'])
    def index() -> str:
        '''This function is the index page of the website.'''

        if request.method == 'POST':
            url_text: str = request.form.get('user_url_input')
            date_added: datetime = datetime.now()

            print(f"date_added: {date_added}")
            print(f"url_text: {url_text}")

        return render_template('index.html')

    return app
