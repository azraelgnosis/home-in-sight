from flask import (
    Blueprint, render_template
)

bp = Blueprint("social", __name__)

@bp.route('/fb/', methods=('GET',))
def fb():
    return render_template('fb.html')