from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from werkzeug.exceptions import abort

from gamr.db import get_db


bp = Blueprint('tables', __name__)


@bp.route('/tables')
def table_index():
    return render_template('tables.html')
