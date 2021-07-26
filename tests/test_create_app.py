from sqlalchemy.sql.expression import select

from flask_blog.orm.db import get_db
from flask_blog.orm.user import User
from tests.data import add_data, get_users

session_factory = None


def test_create_app(app):
    db_session = get_db()
    add_data(get_users())
    query = select(User)

    users = db_session.execute(query).scalars().all()

    assert len(users) == 2


def test_create_another_app(app):
    db_session = get_db()
    add_data(get_users())
    query = select(User)

    users = db_session.execute(query).scalars().all()

    assert len(users) == 2
