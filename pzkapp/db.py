import sqlite3
import os

import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


@click.command('build-clubs')
@with_appcontext
def build_clubs_command():
    """Add clubs to database."""
    db = get_db()

    import csv
    APP_ROOT = os.path.dirname(os.path.abspath(__file__))
    clubs_file = os.path.join(APP_ROOT, 'clubs.csv')

    counter = 0
    with open(clubs_file) as csvfile:
        c = csv.reader(csvfile)
        for club in c:
            name = club[0]
            abbrev = club[1]
            email = club[2]
            magic = club[3]
            try:
                db.execute(
                    "INSERT INTO club (name, email, abbrev, magic) VALUES (?, ?, ?, ?)",
                    (name, email, abbrev, magic.upper()),
                )
                counter += 1
            except db.IntegrityError:
                click.echo(f"Klub {name} istnieje w bazie.")
    db.commit()


    click.echo(f'{counter} clubs added.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(build_clubs_command)
