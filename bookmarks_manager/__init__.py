# author: Gustavo Sopena
# date started: 2024-08-10 at 1530

import os
from datetime import datetime
from flask import Flask, redirect, render_template, request, url_for
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

    @app.route('/', methods=['GET'])
    def index() -> str:
        '''This function is the index page of the website.'''

        return render_template('index.html')

    @app.route('/add', methods=['GET', 'POST'])
    def add() -> str:
        ''''''

        if request.method == 'POST':
            url_name: str | None = request.form.get('name_input')
            url_text: str | None = request.form.get('url_input')
            date_added: datetime = datetime.now()

            new_url: URL_Text = URL_Text(
                name=url_name,
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
            
            return redirect('/add')
        else:
            return render_template('add.html')

    @app.route('/list_urls', methods=['GET'])
    def list_urls() -> str:
        '''This function is the view_urls page of the website.'''
        
        saved_urls = URL_Text.query.order_by(URL_Text.date_added).all()

        return render_template('list_urls.html', saved_urls=saved_urls)
    
    @app.route('/download/<int:url_id>', methods=['GET'])
    def download(url_id: int) -> str:
        '''This function is the download page of the website.'''

        # if request.method == 'POST':
            # url_text: str | None = request.form.get('url_to_send')

        wanted_url: URL_Text = URL_Text.query.get(url_id)
        return render_template('download.html', url_name=wanted_url.name, url_text=wanted_url.url_text)
    
    @app.route('/delete/<int:url_id>', methods=['GET'])
    def delete(url_id: int) -> str:
        '''This function deletes the url from the database.'''
    
        url_to_delete: URL_Text = URL_Text.query.get(url_id)

        try:
            db_session.delete(url_to_delete)
            db_session.commit()
        except:
            return 'There was on error deleting the URL.'
        
        return redirect(url_for('list_urls'))
    
    @app.route('/update/<int:url_id>', methods=['GET', 'POST'])
    def update(url_id: int) -> str:
        '''This function updates the content of the url and stores it the database.'''
        
        url_to_update: URL_Text = URL_Text.query.get(url_id)

        if request.method == 'GET':
            # render the page with the text input pre-filled
            return render_template('update.html', url_item=url_to_update)
        elif request.method == 'POST':
            # update the database with the new value and go to the list view
            url_text = request.form.get('user_url_input')
            url_to_update.url_text = url_text
            url_to_update.has_image = URL_Text.contains_image_extension(url_text)

            try:
                db_session.commit()
            except:
                return 'There was an issue updating the URL.'

            return redirect(url_for('list_urls'))

    return app
