from flask_blog.orm.db import get_db


def test_scoped_sessions(app):
    session1 = get_db()
    session2 = get_db()

    assert session1 is session2
