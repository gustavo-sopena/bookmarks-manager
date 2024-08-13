# author: Gustavo Sopena
# date started: 2024-08-11 at 1747

import click
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base

engine = create_engine('sqlite:///instance/data.db')
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

def shutdown_session(e=None) -> None:
        '''This function removes the current database session.'''

        db_session.remove()

def init_db() -> None:
    '''This function initializes the database by creating the table of data modeled after the python class.'''

    from bookmarks_manager import models
    Base.metadata.create_all(bind=engine)

@click.command('init_db')
def command_init_db() -> None:
    '''This function defines a command that integrates with flask so that the database can be created.'''

    init_db()
    click.echo('Initialized the database.')

def register_database(app) -> None:
    '''This function registers the function 'command_init_db' and 'shutdown_session' with the application.'''

    app.teardown_appcontext(shutdown_session)
    app.cli.add_command(command_init_db)
