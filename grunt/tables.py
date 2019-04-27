from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from werkzeug.exceptions import abort

from grunt.db import get_db


bp = Blueprint('tables', __name__)


@bp.route('/tables')
def table_index():
    db = get_db()

    characters = db.execute(
        'SELECT * FROM character'
    ).fetchall()

    weapons = db.execute(
        'SELECT * FROM equipped_weapon'
    ).fetchall()

    zones = db.execute(
        'SELECT * FROM zone'
    ).fetchall()

    return render_template('tables.html',
        characters=characters, weapons=weapons, zones=zones)

