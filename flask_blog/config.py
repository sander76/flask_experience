from pathlib import Path

from pydantic import BaseSettings

SQLITE_FILE = Path(__file__).parent / "data" / "flask_blog.sqlite"
SQLITE_FILE.parent.mkdir(exist_ok=True, parents=True)


# todo: add secret for securely signing cookies.
class Settings(BaseSettings):
    class Config:
        env_prefix = "flask_blog_"

    database_url: str = f"sqlite+pysqlite:///{SQLITE_FILE.as_posix()}"
    """By default the sqlite connection is used.

    If an environment variable of `flask_blog_database_url` is encountered,
    that one is used instead.
    """

    TESTING: bool = False
    DEVELOPMENT: bool = False
