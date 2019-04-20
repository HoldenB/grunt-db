from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from werkzeug.exceptions import abort

from gamr.auth import login_required
from gamr.db import get_db

bp = Blueprint('characters', __name__)


class CharacterRequest:
    def __init__(self, request):
        self.character_name = request.form['character_name']
        self.character_level = request.form['character_level']
        self.hours_played = request.form['hours_played']
        self.character_kills = request.form['character_kills']
        self.equipped_weapon_id = self.__e_wep_id(request.form['equipped_weapon'])
        
    def __e_wep_id(self, name):
        e_wep_id = get_db().execute(
            'SELECT id FROM equipped_weapon WHERE weapon_name=?',
            (name,)
        ).fetchone()

        # We expect a single column from the sqlite object
        return e_wep_id[0]

    def valid(self):
        return(self.character_name and self.character_level and self.hours_played
                and self.character_kills and self.equipped_weapon_id)


def get_character(id, check_user=True):
    character = get_db().execute(
        'SELECT c.id, e_wep_id, c.user_id, created, hours_played, character_name,'
        ' character_level, character_kills'
        ' FROM character c JOIN user u ON c.user_id = u.id'
        ' WHERE c.id = ?',
        (id,)
    ).fetchone()

    if character is None:
        abort(404, "Character id {0} does not exist.".format(id))

    if character['user_id'] is None:
        abort(404, "User id not found within Character table.")

    if check_user and character['user_id'] != g.user['id']:
        abort(403)

    return character


@bp.route('/')
def character_index():
    db = get_db()
    # Show all characters created by the given user along with their
    # equipped weapons and the zone in which they are found
    characters = db.execute(
        'SELECT c.id, e_wep_id, c.user_id, c.created, hours_played, character_name,'
        ' character_level, character_kills, u.username, e.weapon_name, rarity, zone_name'
        ' FROM character c JOIN user u JOIN equipped_weapon e JOIN zone z'
        ' ON c.user_id = u.id AND c.e_wep_id = e.id AND e.zone_id = z.id'
        ' ORDER BY c.created DESC'
    ).fetchall()

    return render_template('characters/character_index.html', characters=characters)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        character = CharacterRequest(request)
        error = None

        if not character.valid():
            error = 'All fields are required to create a character.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            # When a new character is created, we will default
            # the character to the starting zone with a starter weapon
            db.execute(
                'INSERT INTO character (e_wep_id, user_id, hours_played, character_name,'
                ' character_level, character_kills)'
                ' VALUES (?, ?, ?, ?, ?, ?)',
                (character.equipped_weapon_id, g.user['id'], character.hours_played,
                    character.character_name, character.character_level,
                    character.character_kills)
            )
            db.commit()

            return redirect(url_for('characters.character_index'))

    # If the request method is GET request, we will queue for our weapon list
    # and populate the available weapons to allow the character to equip
    db = get_db()
    # Query for weapon data
    weapon_names = db.execute (
        'SELECT e.weapon_name'
        ' FROM equipped_weapon e'
    ).fetchall()

    return render_template('characters/character_create.html',
        weapon_names=weapon_names)


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    character = get_character(id)

    if request.method == 'POST':
        character = CharacterRequest(request)
        error = None

        if not character.valid():
            error = 'All fields are required to update a character.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE character SET e_wep_id = ?, hours_played = ?,'
                ' character_name = ?, character_level = ?, character_kills = ?'
                ' WHERE id = ?',
                (character.equipped_weapon_id, character.hours_played,
                    character.character_name, character.character_level,
                    character.character_kills, id)
            )
            db.commit()
            return redirect(url_for('characters.character_index'))

    weapon_name = get_db().execute(
        'SELECT weapon_name FROM equipped_weapon WHERE id=?',
        (character['e_wep_id'],)
    ).fetchone()

    weapon_names = get_db().execute(
        'SELECT e.weapon_name '
        ' FROM equipped_weapon e'
    ).fetchall()

    return render_template('characters/character_update.html',
        character=character, weapon_name=weapon_name[0], weapon_names=weapon_names)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_character(id)
    db = get_db()
    db.execute('DELETE FROM character WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('characters.character_index'))
