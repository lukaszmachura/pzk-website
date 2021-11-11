import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from pzkapp.db import get_db

# Blueprint for authentofication
bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        magic = request.form['magic']
        db = get_db()
        error = None

        if not email:
            error = 'Podaj email.'
        elif not password:
            error = 'Podaj hasło.'
        elif not magic:
            error = 'Podaj kod klubu.'

        club = db.execute(
            'SELECT * FROM club WHERE magic = ?', (magic.upper(),)
        ).fetchone()

        if not club:
            error = 'Kod klubu nieprawidłowy.'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO member (email, password, club, club_id) VALUES (?, ?, ?, ?)",
                    (email, generate_password_hash(password), club['name'], club['id']),
                )
                db.commit()
            except db.IntegrityError:
                error = f"Użytkownik o semailu {email} jest już zarejestrowany."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        db = get_db()
        error = None

        user = db.execute(
            'SELECT * FROM member WHERE email = ?', (email,)
        ).fetchone()

        if user is None:
            error = 'Niewłaściwy email.'
        elif not check_password_hash(user['password'], password):
            error = 'Niewłaściwe hasło.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('member.player'))

        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        db = get_db()
        g.user = db.execute(
            'SELECT * FROM member WHERE id = ?', (user_id,)
        ).fetchone()

        # if logged in, fetch user's club
        if g.user:
            g.user_club = db.execute(
                'SELECT * FROM club WHERE id = ?', (g.user['club_id'],)
            ).fetchone()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    '''dekorator dla funkcji modyfikujących www'''
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view


@bp.route('/')
def index():
    return render_template('auth/login.html')
