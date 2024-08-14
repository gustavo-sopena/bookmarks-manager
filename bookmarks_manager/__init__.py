# author: Gustavo Sopena
# date started: 2024-08-10 at 1530

import os
from datetime import datetime
from flask import Flask, redirect, render_template, request
from bookmarks_manager.models import URL_Text

def create_app(test_config=None) -> Flask:
    '''This function will create the Flask application.'''

    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from bookmarks_manager.db import register_database, db_session
    register_database(app)

    @app.route('/', methods=['GET', 'POST'])
    def index() -> str:
        '''This function is the index page of the website.'''

        if request.method == 'POST':
            url_text: str | None = request.form.get('user_url_input')
            date_added: datetime = datetime.now()

            new_url: URL_Text = URL_Text(
                url_text=url_text,
                date_added=date_added,
                has_image=URL_Text.contains_image_extension(url_text)
            )
            print(new_url)

            try:
                db_session.add(new_url)
                db_session.commit()
            except Exception as e:
                print(f'Error: {e}')
            
            return redirect('/')
        else:
            return render_template('index.html')

    @app.route('/list_urls', methods=['GET'])
    def list_urls() -> str:
        '''This function is the view_urls page of the website.'''
        
        saved_urls = URL_Text.query.order_by(URL_Text.date_added).all()

        return render_template('list_urls.html', saved_urls=saved_urls)
    
    @app.route('/download', methods=['POST'])
    def download() -> str:
        '''This function is the download page of the website.'''

        if request.method == 'POST':
            url_text: str | None = request.form.get('url_to_send')
    
        return url_text

    return app
