"""Flask entrypoint"""
import logging
from pathlib import Path

from flask import Flask

from . import auth, blog, db

_LOGGER = logging.getLogger(__name__)


def create_app(test_config=None):
    """Create and configure the app."""

    app = Flask(__name__, instance_relative_config=True)
    _LOGGER.info("Instance path: %s", app.instance_path)
    app.config.from_mapping(
        SECRET_KEY="dev", DATABASE=Path(app.instance_path).joinpath("flask_blog.sqlite")
    )

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    # ensure th instance folder exists.
    Path(app.instance_path).mkdir(exist_ok=True, parents=True)

    @app.route("/hello")
    def hello():
        return "Hello you."

    db.init_app(app)

    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)
    app.add_url_rule("/", endpoint="index")  # type: ignore

    return app
