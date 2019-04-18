from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from werkzeug.exceptions import abort

from gamr.auth import login_required
from gamr.db import get_db


bp = Blueprint('zones', __name__)


def get_zone(id, check_zone=True):
    zone = get_db().execute(
        'SELECT z.id, z.user_id, created, num_characters, num_creatures'
        ' zone_name, zone_level_range, difficulty'
        ' FROM zone z JOIN user u ON z.user_id = u.id'
        ' WHERE z.id = ?',
        (id,)
    ).fetchone()

    if zone is None:
        abort(404, "Zone id {0} does not exist.".format(id))

    if zone['user_id'] is None:
        abort(404, "User id not found within Zone table.")

    if check_zone and zone['user_id'] != g.user['id']:
        abort(403)

    return zone


@bp.route('/zones')
def zone_index():
    db = get_db()
    # Query for zone data
    zones = db.execute (
        'SELECT *'
        ' FROM zone z'
        ' ORDER BY z.created DESC'
    ).fetchall()

    return render_template('zones/zone_index.html', zones=zones)


@bp.route('/zones/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        zone_name = request.form['zone_name']
        error = None

        if not zone_name:
            error = 'Zone name is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO zone (zone_name, user_id, zone_level_range, difficulty,'
                ' num_creatures, num_characters)'
                ' VALUES (?, ?, ?, ?, ?, ?)',
                (zone_name, g.user['id'], '1-20', 'Easy', 1, 1)
            )
            db.commit()

            return redirect(url_for('zones.zone_index'))

    return render_template('zones/zone_create.html')


@bp.route('/<int:id>/zones/update', methods=('GET', 'POST'))
@login_required
def update(id):
    zone = get_zone(id)

    if request.method == 'POST':
        zone_name = request.form['zone_name']
        error = None

        if not zone_name:
            error = 'Zone name is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE zone SET zone_name = ?'
                ' WHERE id = ?',
                (zone_name, id)
            )
            db.commit()
            return redirect(url_for('zones.zone_index'))

    return render_template('zones/zone_update.html', zone=zone)


@bp.route('/<int:id>/zones/delete', methods=('POST',))
@login_required
def delete(id):
    get_zone(id)
    db = get_db()
    db.execute('DELETE FROM zone WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('zones.zone_index'))
