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
            click.echo(f'{type(club)}')
            try:
                int(get_col_from_row(club, 0))
            except:
                continue
            name = get_col_from_row(club, 1)
            abbrev = get_col_from_row(club, 2)
            email = get_col_from_row(club, 3)
            address = get_col_from_row(club, 4)
            phone = get_col_from_row(club, 5)
            www = get_col_from_row(club, 6)
            fb = get_col_from_row(club, 7)
            magic = get_col_from_row(club, 8)
            try:
                db.execute(
                    "INSERT INTO club (name, email, abbrev, magic, address, phone, www, fb) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (name, email, abbrev, magic.upper(), address, phone, www, fb),
                )
                counter += 1
            except db.IntegrityError:
                click.echo(f"Klub {name} istnieje w bazie.")
    db.commit()
    click.echo(f'{counter} clubs added.')


def get_col_from_row(row, col):
    try:
        c = row[col]
    except:
        c = 'TBA'
    return c
