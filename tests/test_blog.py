import pytest
from flask import Response
from sqlalchemy.sql.expression import select

from flask_blog.orm.db import get_db
from flask_blog.orm.post import Post
from flask_blog.services import blog_post_service
from tests import data


def test_index(client, auth):
    session = get_db()
    data.add_data(data.get_users())

    response = client.get("/")
    assert b"Log In" in response.data
    assert b"Register" in response.data

    auth.login()
    response = client.get("/")
    assert b"Log Out" in response.data
    assert b"Register" not in response.data

    session.close()
    # assert b"test title" in response.data
    # assert b"by test on 2018-01-01" in response.data
    # assert b"test\nbody" in response.data
    # assert b'href="/1/update"' in response.data


@pytest.mark.parametrize(
    "path",
    (
        "/create",
        "/1/update",
        "/1/delete",
    ),
)
def test_login_required(client, path):
    response = client.post(path)
    assert response.headers["Location"] == "http://localhost/auth/login"


def test_author_required(app, client, auth):
    data.add_data(data.get_users(), data.get_posts())
    # change the post author to another user
    with app.app_context():
        db = get_db()
        db.execute("UPDATE post SET author_id = 1 WHERE id = 2")
        db.commit()

    auth.login()
    # current user can't modify other user's post
    assert client.post("/1/update").status_code == 403
    # current user doesn't see edit link
    assert b'href="/1/update"' not in client.get("/").data


@pytest.mark.parametrize(
    "path",
    (
        "/2/update",
        "/2/delete",
    ),
)
def test_exists_required(client, auth, path):
    data.add_data(data.get_users())
    auth.login()

    assert client.post(path).status_code == 404


def test_create(client, auth, app):
    session = get_db()
    print(f"session at start {session}")
    data.add_data(data.get_users())
    auth.login()

    assert client.get("/create").status_code == 200
    client.post("/create", data={"title": "Alone on the wall.", "body": "Scary story."})

    session = get_db()
    posts = blog_post_service.latest_posts(session)

    assert len(posts) == 1

    post = posts[-1]

    assert post.body == "Scary story."
    assert post.title == "Alone on the wall."


def test_update_success(client, auth, app):
    data.add_data(data.get_users(), data.get_posts())
    db_session = get_db()
    # by default logged in as Graham.
    auth.login()

    assert client.get("/2/update").status_code == 200

    client.post("/2/update", data={"title": "updated", "body": ""})

    post = blog_post_service.get_post(2)
    assert post.title == "updated"

    db_session.close()


def test_update_user_not_creator_of_post(client, auth, app):
    """A user who does not own the post is not allowed to do this."""

    data.add_data(data.get_users(), data.get_posts())

    auth.login()
    response: Response = client.get("/1/update")

    assert response.status_code == 403


def test_update_non_existing_post(client, auth, app):
    data.add_data(data.get_users())

    auth.login()
    response = client.get("/1/update")

    assert response.status_code == 404


@pytest.mark.parametrize(
    "path",
    (
        "/create",
        "/2/update",
    ),
)
def test_create_update_validate(client, auth, path):
    data.add_data(data.get_users(), data.get_posts())
    auth.login()

    response = client.post(path, data={"title": "", "body": ""})

    assert b"Title is required." in response.data


def test_delete(client, auth, app):
    data.add_data(data.get_users(), data.get_posts())
    auth.login()
    post_id = 2
    db_session = get_db()

    response = client.post(f"/{post_id}/delete")

    assert response.headers["Location"] == "http://localhost/"

    query = select(Post).filter(Post.id == post_id)
    post = db_session.execute(query).scalar_one_or_none()
    assert post is None
