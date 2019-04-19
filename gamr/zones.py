from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from werkzeug.exceptions import abort

from gamr.auth import login_required
from gamr.db import get_db


bp = Blueprint('zones', __name__)


class ZoneRequest:
    def __init__(self, request):
        self.zone_name = request.form['zone_name']
        self.num_creatures = request.form['num_creatures']
        self.num_characters = request.form['num_characters']
        self.zone_level_range_min = request.form['zone_level_range_min']
        self.zone_level_range_max = request.form['zone_level_range_max']
        self.difficulty = request.form['difficulty']

    def valid(self):
        return(self.zone_name and self.num_creatures and self.num_characters
                and self.zone_level_range_min and self.zone_level_range_max)


def get_zone(id, check_zone=True):
    zone = get_db().execute(
        'SELECT *'
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
        zone = ZoneRequest(request)
        error = None

        if not zone.valid():
            error = 'All fields are required to create a zone.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO zone (user_id, num_characters, num_creatures,'
                ' zone_name, zone_level_range_min, zone_level_range_max, difficulty)'
                ' VALUES (?, ?, ?, ?, ?, ?, ?)',
                (g.user['id'], zone.num_characters, zone.num_creatures, zone.zone_name, \
                    zone.zone_level_range_min, zone.zone_level_range_max, zone.difficulty)
            )
            db.commit()

            return redirect(url_for('zones.zone_index'))

    return render_template('zones/zone_create.html')


@bp.route('/<int:id>/zones/update', methods=('GET', 'POST'))
@login_required
def update(id):
    zone = get_zone(id)

    if request.method == 'POST':
        zone = ZoneRequest(request)
        error = None

        if not zone.valid():
            error = 'All fields are required to update a zone.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE zone SET num_characters = ?, num_creatures = ?,'
                ' zone_name = ?, zone_level_range_min = ?, zone_level_range_max = ?,'
                ' difficulty = ?'
                ' WHERE id = ?',
                (zone.num_characters, zone.num_creatures, zone.zone_name, \
                    zone.zone_level_range_min, zone.zone_level_range_max, \
                    zone.difficulty, id)
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
