import functools
import logging

from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from flask_blog.orm.db import get_db
from flask_blog.services import user_service
from flask_blog.view_models.auth_view_model import LoginViewModel, RegisterViewModel

_LOGGER = logging.getLogger(__name__)

bp = Blueprint("auth", __name__, url_prefix="/auth")

#  todo: add flask-login


@bp.route("/register", methods=("GET", "POST"))
def register():
    if request.method == "POST":

        view_model = RegisterViewModel(request)
        view_model.load()

        if view_model.error:
            flash(view_model.error)
        else:
            view_model.create_user()
            return redirect(url_for("auth.login"))

    # todo: Prevent user to enter all new data, if previous password or name was wrong.
    return render_template("register.jinja")


@bp.route("/login", methods=("GET", "POST"))
def login():

    if request.method == "POST":
        view_model = LoginViewModel(request)
        view_model.load()

        if view_model.error:
            flash(view_model.error)

        else:
            db_session = get_db()

            user = user_service.get_user_by_name(db_session, view_model.username)
            assert user is not None
            session.clear()

            # store the user id in a session.
            # Flask also securely stores this in a cookie.
            # https://flask.palletsprojects.com/en/2.0.x/api/#sessions
            session["user_id"] = user.id
            return redirect(url_for("index"))

    return render_template("login.jinja")


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        _LOGGER.debug("Get user by user_id which is stored in the session.")
        g.user = user_service.get_user_by_id(user_id)


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


def login_required(view):
    """Check if a user is logged in.

    Wrap this as a decorator around a view function to make sure
    this function is only executed if a user is logged in.
    """

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view
