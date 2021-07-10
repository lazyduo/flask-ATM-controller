import functools

from flask import(
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from atm.db import get_db

bp = Blueprint('atm', __name__)

@bp.route('/')
def index():
    db = get_db()

    account_id = session.get('account_id')

    balance = 'null'
    if account_id:
        balance = db.execute(
            'SELECT balance FROM account WHERE id =?', (session['account_id'],)
        ).fetchone()

    return render_template('atm/index.html', balance=balance)

@bp.route('/<int:id>/deposit', methods=('POST',))
def deposit(id):
    deposit = request.form['deposit']
    db = get_db()
    account = db.execute(
        'SELECT * FROM account WHERE id = ?', (id,)
    ).fetchone()

    update_balance = account['balance'] + int(deposit)
    db.execute(
        'UPDATE account SET balance = ?'
        ' WHERE id = ?',
        (update_balance, id)
    )
    db.commit()

    return redirect(url_for('atm.index'))

@bp.route('/<int:id>/withdraw', methods=('POST',))
def withdraw(id):
    withdraw = request.form['withdraw']
    db = get_db()
    account = db.execute(
        'SELECT * FROM account WHERE id = ?', (id,)
    ).fetchone()
    
    update_balance = account['balance'] - int(withdraw)
    db.execute(
        'UPDATE account SET balance = ?'
        ' WHERE id = ?',
        (update_balance, id)
    )
    db.commit()

    return redirect(url_for('atm.index'))

@bp.before_app_request
def load_logged_in_user():
    account_id = session.get('account_id')

    if account_id is None:
        g.account = None
    else:
        g.account = get_db().execute(
            'SELECT * FROM account WHERE id = ?', (account_id,)
        ).fetchone()