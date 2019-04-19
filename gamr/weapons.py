from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from werkzeug.exceptions import abort

from gamr.auth import login_required
from gamr.db import get_db


bp = Blueprint('weapons', __name__)


class WeaponRequest:
    def __init__(self, request):
        self.weapon_name = request.form['weapon_name']
        self.weapon_type = request.form['weapon_type']
        self.weapon_level = request.form['weapon_level']
        self.rarity = request.form['rarity']
        self.zone_id = self.__zone_id(request.form['zone_name'])
        
    def __zone_id(self, name):
        z_id = get_db().execute(
            'SELECT id FROM zone WHERE zone_name=?',
            (name,)
        ).fetchone()

        # We expect a single column from the sqlite object
        return z_id[0]

    def valid(self):
        return(self.weapon_name and self.weapon_type and self.weapon_level
                and self.rarity)


def get_equipped_weapon(id, check_weapon=True):
    weapon = get_db().execute(
        'SELECT e.id, e.user_id, created, weapon_name'
        ' weapon_level, weapon_type, rarity'
        ' FROM equipped_weapon e JOIN user u ON e.user_id = u.id'
        ' WHERE e.id = ?',
        (id,)
    ).fetchone()

    if weapon is None:
        abort(404, "Weapon id {0} does not exist.".format(id))

    if weapon['user_id'] is None:
        abort(404, "User id not found within weapon table.")

    if check_weapon and weapon['user_id'] != g.user['id']:
        abort(403)

    return weapon


@bp.route('/weapons')
def weapon_index():
    db = get_db()
    # Query for weapon data joined with zone data
    # in order for us to get the zone in which the weapon is found
    weapons = db.execute(
        'SELECT *'
        ' FROM equipped_weapon e JOIN zone z'
        ' ON e.zone_id = z.id'
        ' ORDER BY e.created DESC'
    ).fetchall()

    return render_template('weapons/weapon_index.html', weapons=weapons)


@bp.route('/weapons/create', methods=('GET', 'POST'))
@login_required
def create():
    # on a POST request, we need to also acquire the zone ID from the selected
    # available zone name, our WeaponRequest object will help us with this
    if request.method == 'POST':
        weapon = WeaponRequest(request)
        error = None

        if not weapon.valid():
            error = 'All fields are required to crate a weapon.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO equipped_weapon (user_id, zone_id, weapon_name,'
                ' weapon_level, weapon_type, rarity)'
                ' VALUES (?, ?, ?, ?, ?, ?)',
                (g.user['id'], weapon.zone_id, weapon.weapon_name, weapon.weapon_level, \
                    weapon.weapon_type, weapon.rarity)
            )
            db.commit()

            return redirect(url_for('weapons.weapon_index'))

    # If the request method is GET request, we will queue for our zone list
    # and populate the available zones to place this weapon
    db = get_db()
    # Query for zone data
    zone_names = db.execute (
        'SELECT z.zone_name'
        ' FROM zone z'
    ).fetchall()

    # Note: zone_name will contain sqlite objects with a single column, so we need
    # to access this in the templating by 'for zone_name[0] in zone_names'
    return render_template('weapons/weapon_create.html', zone_names=zone_names)


@bp.route('/<int:id>/weapons/update', methods=('GET', 'POST'))
@login_required
def update(id):
    weapon = get_equipped_weapon(id)

    if request.method == 'POST':
        weapon_name = request.form['weapon_name']
        error = None

        if not weapon_name:
            error = 'Weapon name is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE equipped_weapon SET weapon_name = ?'
                ' WHERE id = ?',
                (weapon_name, id)
            )
            db.commit()
            return redirect(url_for('weapons.weapon_index'))

    return render_template('weapons/weapon_update.html', weapon=weapon)


@bp.route('/<int:id>/weapons/delete', methods=('POST',))
@login_required
def delete(id):
    get_equipped_weapon(id)
    db = get_db()
    db.execute('DELETE FROM equipped_weapon WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('weapons.weapon_index'))
