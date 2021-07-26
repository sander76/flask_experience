"""Database."""

import logging
from typing import Callable, Optional

from sqlalchemy import create_engine, orm
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm.session import Session

from flask_blog.orm.modelbase import SqlAlchemyBase

_LOGGER = logging.getLogger(__name__)


__session_factory: Optional[Callable[[], Session]] = None


def init_app(app):
    app.teardown_appcontext(close_session)


def close_session(exception=None):
    if __session_factory:
        __session_factory.remove()


def init_db(connection_url: str):
    """Initialize the database.

    Using the declarative approach.

    https://flask.palletsprojects.com/en/2.0.x/patterns/sqlalchemy/#declarative
    """
    global __session_factory

    if __session_factory:
        _LOGGER.info("Session factory already initialized.")
        raise Exception("you should run this function only once.")

    _LOGGER.info("Creating sqlalchemy engine connection to %s", connection_url)
    engine = create_engine(connection_url, future=True)

    # using scoped_session factory. Allows for calling get_db multiple times,
    # but always returning the same session within the same thread.
    __session_factory = scoped_session(orm.sessionmaker(bind=engine))

    import flask_blog.orm.__all_models  # noqa

    SqlAlchemyBase.metadata.create_all(bind=engine)


def close_db():
    global __session_factory
    if __session_factory:
        __session_factory.remove()
    __session_factory = None


def get_db() -> Session:
    """Return a session object.

    It is best practice to call this at each new user request and close it
    when this request is done.

    https://docs.sqlalchemy.org/en/14/orm/session_basics.html#when-do-i-construct-a-session-when-do-i-commit-it-and-when-do-i-close-it
    """

    if not __session_factory:
        raise Exception("database not initialized. run `init_db` first ?")

    session: Session = __session_factory()
    return session
