from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from werkzeug.exceptions import abort

from gamr.auth import login_required
from gamr.db import get_db

bp = Blueprint('zones', __name__)

@bp.route('/zones')
def zone_index():
    return render_template('zones/zone_index.html')

@bp.route('/', methods=('GET', 'POST'))
def create():
    return redirect(url_for('zones.zone_index'))
