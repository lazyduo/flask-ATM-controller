import functools

from flask import(
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from atm.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        card_number = request.form['card_number']
        pin_number = request.form['pin_number']
        db = get_db()
        error = None

        if not card_number:
            error = 'Card_number is required.'
        elif not username:
            error = 'Usernname is required.'
        elif not pin_number:
            error = 'pin_number is required.'
        elif db.execute(
            'SELECT id FROM account WHERE card_number = ?', (card_number,)
        ).fetchone() is not None:
            error = f"Card Number {card_number} is already registered."
        
        if error is None:
            db.execute(
                'INSERT INTO account (username, card_number, pin_number) VALUES (?, ?, ?)',
                (username, card_number, generate_password_hash(pin_number))
            )
            db.commit()
            return redirect(url_for('auth.login'))
        
        flash(error)
    
    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        card_number = request.form['card_number']
        pin_number = request.form['pin_number']
        db = get_db()
        error = None
        account = db.execute(
            'SELECT * FROM account WHERE card_number = ?', (card_number,)
        ).fetchone()

        if account is None:
            error = 'Incorrect Card number.'
        elif not check_password_hash(account['pin_number'], pin_number):
            error = 'Incorrect PIN number.'
        if error is None:
            session.clear()
            session['account_id'] = account['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    account_id = session.get('account_id')

    if account_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM account WHERE id = ?', (account_id,)
        ).fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        
        return view(**kwargs)
    
    return wrapped_view