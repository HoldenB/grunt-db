from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from werkzeug.exceptions import abort

from gamr.auth import login_required
from gamr.db import get_db

bp = Blueprint('weapons', __name__)

@bp.route('/weapons')
def weapon_index():
    return render_template('weapons/weapon_index.html')

@bp.route('/', methods=('GET', 'POST'))
def create():
    return redirect(url_for('weapons.weapon_index'))
