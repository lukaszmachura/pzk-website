import sqlite3
import os
import click
from flask import current_app, g
from flask.cli import with_appcontext
import csv
from datetime import datetime


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

    APP_ROOT = os.path.dirname(os.path.abspath(__file__))
    clubs_file = os.path.join(APP_ROOT, 'club.csv')

    counter = 0
    with open(clubs_file) as csvfile:
        c = csv.reader(csvfile)
        for club in c:
            try:
                int(club[0])
                db.execute(  # the order is crucial
                    "INSERT INTO club (name, abbrev, email, address, phone, www, fb, magic) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    club[1:]
                )
                counter += 1
            except db.IntegrityError:
                click.echo(f"Klub {club[1]} istnieje w bazie.")
            except ValueError:
                click.echo(f'fields: {club}')  # catch header
    db.commit()
    click.echo(f'{counter} clubs added.')


def save_db_as_csv(dbname):
    now = datetime.now().strftime("%Y%m%d%H%M%S")
    db = get_db()
    db_cursor = db.cursor()
    db_cursor.execute(f'SELECT * FROM {dbname}')
    with open(f'pzk_{dbname}_{now}.csv', 'w') as out_csv_file:
      csv_out = csv.writer(out_csv_file)  #, delimiter=';')
      # write header
      csv_out.writerow([d[0] for d in db_cursor.description])
      # write data
      for result in db_cursor:
        csv_out.writerow(result)
    db.close()


@click.command('club-to-csv')
@with_appcontext
def clubs_to_csv_command():
    save_db_as_csv('club')

@click.command('member-to-csv')
@with_appcontext
def member_to_csv_command():
    save_db_as_csv('member')

@click.command('event-to-csv')
@with_appcontext
def event_to_csv_command():
    save_db_as_csv('event')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(build_clubs_command)
    app.cli.add_command(clubs_to_csv_command)
    app.cli.add_command(member_to_csv_command)
    app.cli.add_command(event_to_csv_command)
