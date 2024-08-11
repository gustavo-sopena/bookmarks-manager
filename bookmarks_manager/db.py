# author: Gustavo Sopena
# date started: 2024-08-10 at 2040

import sqlite3
import click
from flask import Flask, current_app, g

def get_database():
    '''This function gets the database from the current application handling the request.'''

    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def close_database(e=None) -> None:
    '''This function closes the connection to the database.'''

    db: sqlite3.Connection = g.pop('db', None)

    if db is not None:
        db.close()

def initialize_database() -> None:
    '''This function initializes the database.'''

    db: sqlite3.Connection = get_database()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

@click.command('initialize_database_command')
def initialize_database_command() -> None:
    '''This function executes a script that either creates or resets the database.'''

    initialize_database()
    click.echo('Initialized the database.')

def register_database(app: Flask) -> None:
    '''This function registers the 'initialize_database_command' and 'close_database' with the application.'''

    app.teardown_appcontext(close_database)
    app.cli.add_command(initialize_database_command)
