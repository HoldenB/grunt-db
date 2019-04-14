from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from werkzeug.exceptions import abort

from gamr.auth import login_required
from gamr.db import get_db

bp = Blueprint('characters', __name__)


@bp.route('/')
def character_index():
    db = get_db()
    # Show all characters created by the given user
    characters = db.execute(
        'SELECT c.id, e_wep_id, user_id, c.created, hours_played, character_name, character_level, character_kills, u.username, e.weapon_name, rarity, zone_name'
        ' FROM character c JOIN user u JOIN equipped_weapon e JOIN zone z'
        ' ON c.user_id = u.id AND c.e_wep_id = e.id AND e.zone_id = z.id'
        ' ORDER BY c.created DESC'
    ).fetchall()

    return render_template('characters/character_index.html', characters=characters)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        character_name = request.form['character_name']
        error = None

        if not character_name:
            error = 'Character name is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            # When a new character is created, we will default
            # the character to the starting zone with a starter weapon
            db.execute(
                'INSERT INTO character (e_wep_id, user_id, hours_played, character_name, character_level, character_kills)'
                ' VALUES (?, ?, ?, ?, ?, ?)',
                (1, g.user['id'], 0, character_name, 1, 0)
            )
            db.commit()

            return redirect(url_for('characters.character_index'))

    return render_template('characters/create.html')


def get_character(id, check_user=True):
    character = get_db().execute(
        'SELECT c.id, e_wep_id, user_id, created, hours_played, character_name, character_level, character_kills'
        ' FROM character c JOIN user u ON c.user_id = u.id'
        ' WHERE c.id = ?',
        (id,)
    ).fetchone()

    if character is None:
        abort(404, "Character id {0} doesn't exist.".format(id))

    if check_user and character['user_id'] != g.user['id']:
        abort(403)

    return character


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    character = get_character(id)

    if request.method == 'POST':
        character_name = request.form['character_name']
        error = None

        if not character_name:
            error = 'Character name is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE character SET character_name = ?'
                ' WHERE id = ?',
                (character_name, id)
            )
            db.commit()
            return redirect(url_for('characters.character_index'))

    return render_template('characters/update.html', character=character)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_character(id)
    db = get_db()
    db.execute('DELETE FROM character WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('characters.character_index'))
