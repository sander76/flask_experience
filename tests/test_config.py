import os

import pytest

from flask_blog.config import SQLITE_FILE, Settings


def test_config_dbase_url():
    settings = Settings()
    assert str(SQLITE_FILE.as_posix()) in settings.database_url


@pytest.fixture
def dbase_as_env():
    os.environ["flask_blog_database_url"] = "abc"
    yield
    os.environ.pop("flask_blog_database_url")


def test_config_dbase_url_from_env_value(dbase_as_env):
    settings = Settings()
    assert settings.database_url == "abc"
