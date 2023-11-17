import sqlite3

import click
from flask import current_app, g


#: g is a mysterious object unique for each request
#: Current app is present when app factory function has been run


def get_db():
    if 'db' not in g:
        #: Connects to db with key from config
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
        #: Something, something possible to access columns by name
    return g.db


#: Closes bd connection if open
def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


#: Initiates db and runs schema to set up
def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


#: Creates a command line command!
@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')
