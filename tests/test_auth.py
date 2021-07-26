import pytest
from flask import g, session

from tests import data

# from flask_blog.db import get_db


def test_register_get_form(client):
    assert client.get("/auth/register").status_code == 200


def test_register_new_user(client, app):
    """New user registration should redirect to the login page."""
    response = client.post(
        "/auth/register", data={"username": "a", "password": "123456"}
    )
    assert "http://localhost/auth/login" == response.headers["Location"]


def test_login_get_form(client, auth):
    assert client.get("/auth/login").status_code == 200


def test_login_success(client, auth):
    data.add_data(data.get_users())
    response = auth.login()
    assert response.headers["Location"] == "http://localhost/"

    with client:
        client.get("/")
        assert session["user_id"] == 2
        assert g.user.username == "Graham"


@pytest.mark.parametrize(
    ("username", "password", "message"),
    (
        ("wrong_user", "test", b"User does not exist"),
        ("Graham", "a", b"Incorrect password"),
    ),
)
def test_login_validate_input(auth, username, password, message):
    data.add_data(data.get_users())
    response = auth.login(username, password)

    assert message in response.data
