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

    return render_template('blog/index.html')