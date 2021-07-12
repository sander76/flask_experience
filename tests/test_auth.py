import pytest
from flask import g, session

from flask_blog.db import get_db


def test_register_get_form(client):
    assert client.get("/auth/register").status_code == 200


def test_register_new_user(client, app):
    response = client.post("/auth/register", data={"username": "a", "password": "a"})
    assert "http://localhost/auth/login" == response.headers["Location"]

    with app.app_context():
        assert (
            get_db().execute("SELECT * FROM user WHERE username= 'a'").fetchone()
            is not None
        )


def test_login_get_form(client, auth):
    assert client.get("/auth/login").status_code == 200


def test_login_success(client, auth):
    response = auth.login()
    assert response.headers["Location"] == "http://localhost/"

    with client:
        client.get("/")
        assert session["user_id"] == 1
        assert g.user["username"] == "test"


@pytest.mark.parametrize(
    ("username", "password", "message"),
    (("a", "test", b"Incorrect username."), ("test", "a", b"Incorrect password.")),
)
def test_login_validate_input(auth, username, password, message):
    response = auth.login(username, password)

    assert message in response.data
