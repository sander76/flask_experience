from pathlib import Path

import pytest

from flask_blog import create_app
from flask_blog.db import get_db, init_db

HERE = Path(__file__).parent


def _read_sql():
    with open(HERE / "data.sql") as file:
        data = file.read()

    return data


@pytest.fixture
def app(tmp_path):
    dbase_file: Path = tmp_path / "dbase.sqlite"
    app = create_app({"TESTING": True, "DATABASE": dbase_file})

    with app.app_context():
        init_db()
        get_db().executescript(_read_sql())

    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


class AuthActions:
    def __init__(self, client) -> None:
        self._client = client

    def login(self, username="test", password="test"):
        return self._client.post(
            "/auth/login", data={"username": username, "password": password}
        )

    def logout(self):
        return self._client.get("/auth/logout")


@pytest.fixture
def auth(client):
    return AuthActions(client)
