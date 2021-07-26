"""Flask entrypoint"""
from __future__ import annotations

import logging
from pathlib import Path

from flask import Flask

from flask_blog import auth, blog  # noqa
from flask_blog.config import Settings
from flask_blog.orm import db

_LOGGER = logging.getLogger(__name__)


def create_app(settings: Settings | None = None):
    """Create and configure the app."""
    if settings is None:
        settings = Settings()

    _setup_logging()
    _LOGGER.info("Creating the app.")

    app = Flask(__name__, instance_relative_config=True)
    _LOGGER.info("Instance path: %s", app.instance_path)

    _LOGGER.info("Database URL: %s", settings.database_url)
    db.init_db(settings.database_url)
    db.init_app(app)

    app.config.from_mapping(SECRET_KEY="dev")

    # ensure th instance folder exists.
    Path(app.instance_path).mkdir(exist_ok=True, parents=True)

    _config_routes(app)

    return app


def _setup_logging():
    # logger = logging.getLogger()
    # logger.setLevel(level=logging.DEBUG)
    logging.basicConfig(level=logging.DEBUG)


def _config_routes(app):
    """Add all the routes."""

    @app.route("/hello")
    def hello():
        return "Hello you."

    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)
    app.add_url_rule("/", endpoint="index")  # type: ignore
