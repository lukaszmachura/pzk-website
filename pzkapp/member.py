import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from pzkapp.auth import login_required
from pzkapp.db import get_db

# Blueprint for authentofication
bp = Blueprint('member', __name__, url_prefix='/member')

@bp.route('/player') #, methods=('GET', 'POST'))
@login_required
def player():
    user_id = session.get('user_id')
    db = get_db()

    member = db.execute(
        'SELECT * FROM member WHERE id = ?', (user_id,)
    ).fetchone()

    clubs = db.execute(
        'SELECT * FROM club'
    ).fetchall()

    club = db.execute(
        'SELECT * FROM club WHERE id = ?', (member['club_id'], )
    ).fetchone()

    return render_template('member/player.html', member=member, club=club)
