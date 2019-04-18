from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from werkzeug.exceptions import abort

from gamr.auth import login_required
from gamr.db import get_db


bp = Blueprint('weapons', __name__)


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
    # Query for weapon data
    weapons = db.execute (
        'SELECT *'
        ' FROM equipped_weapon w'
        ' ORDER BY w.created DESC'
    ).fetchall()

    return render_template('weapons/weapon_index.html', weapons=weapons)


@bp.route('/weapons/create', methods=('GET', 'POST'))
@login_required
def create():
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
                'INSERT INTO equipped_weapon (weapon_name, user_id, zone_id,'
                ' weapon_level, weapon_type, rarity)'
                ' VALUES (?, ?, ?, ?, ?, ?)',
                (weapon_name, g.user['id'], 1, 1, 'Default', 'Common')
            )
            db.commit()

            return redirect(url_for('weapons.weapon_index'))

    return render_template('weapons/weapon_create.html')


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
