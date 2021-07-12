import sqlite3

import pytest

from flask_blog import db
from flask_blog.db import get_db


def test_get_close_db(app):
    with app.app_context():
        db = get_db()
        assert db is get_db()

    with pytest.raises(sqlite3.ProgrammingError) as e:
        db.execute("SELECT 1")

    assert "closed" in str(e.value)


def test_init_db_command(runner, mocker):
    mocker.patch.object(db, "init_db")

    result = runner.invoke(args=["init-db"])
    assert "Initialized" in result.output

    db.init_db.assert_called()
