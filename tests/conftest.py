from pathlib import Path

import pytest

from flask_blog import create_app
from flask_blog.config import Settings
from flask_blog.orm import db
from flask_blog.orm.user import User
from tests import data

HERE = Path(__file__).parent


@pytest.fixture()
def app(tmp_path):
    """Create an app with a testing database.

    Database is empty.
    Tot populate it (per test function) use the data module in the test package.
    """
    sqlite_file = tmp_path / "dbase.sqlite"
    dbase_file: str = f"sqlite+pysqlite:///{sqlite_file.as_posix()}"

    settings = Settings()

    settings.TESTING = True
    settings.DEVELOPMENT = True
    settings.database_url = dbase_file

    app = create_app(settings)

    yield app

    db.close_db()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


class AuthActions:
    def __init__(self, client) -> None:
        self._client = client
        self.user: User = data.get_users()[-1]

    def login(self, username="Graham", password="the island"):

        return self._client.post(
            "/auth/login", data={"username": username, "password": password}
        )

    def logout(self):
        return self._client.get("/auth/logout")


@pytest.fixture
def auth(client):
    return AuthActions(client)
