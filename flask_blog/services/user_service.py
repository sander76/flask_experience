"""User related service."""

from __future__ import annotations

from sqlalchemy.orm.session import Session
from sqlalchemy.sql.expression import select
from werkzeug.security import generate_password_hash

from flask_blog.orm.db import get_db
from flask_blog.orm.user import User


def get_user_by_name(session: Session, name: str) -> User | None:
    query = select(User).filter(User.username == name)
    result = session.execute(query)

    return result.scalar_one_or_none()


def create_user(session: Session, name: str, password: str):
    """Create a user and store the name and hashed password in the
    database.
    """
    user = User(username=name, password=generate_password_hash(password))
    session.add(user)


def get_user_by_id(id: int) -> User | None:
    """Return a user based on provided index.

    Returns:
        User or None.
    """
    session = get_db()
    query = select(User).filter(User.id == id)
    result = session.execute(query)

    return result.scalar_one_or_none()
