import logging

from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort

from flask_blog.auth import login_required
from flask_blog.orm import post
from flask_blog.orm.db import get_db
from flask_blog.services import blog_post_service
from flask_blog.view_models.blog_view_model import (
    CreateBlogViewModel,
    UpdateBlogViewModel,
)
from flask_blog.view_models.index_view_model import IndexViewModel

_LOGGER = logging.getLogger(__name__)

# from flask_blog.orm.db import get_db

bp = Blueprint("blog", __name__)

# todo: uncomment all functions.


def _get_post(id: int, check_author: bool = True) -> post.Post:
    post = blog_post_service.get_post(id)

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")
    if check_author and post.author_id != g.user.id:
        abort(403)

    return post


@bp.route("/")
def index():
    _LOGGER.debug("getting index")
    model = IndexViewModel(request)
    model.load()

    return render_template("index.jinja", posts=model.posts)


@bp.route("/create", methods=("GET", "POST"))
@login_required
def create():
    if request.method == "POST":

        view_model = CreateBlogViewModel(request)
        view_model.load()

        if view_model.error:
            flash(view_model.error)

        else:
            db_session = get_db()
            blog_post_service.create_post(
                view_model.title, body=view_model.body, author_id=g.user.id
            )
            db_session.commit()

            return redirect(url_for("blog.index"))

    return render_template("create.jinja")


@bp.route("/<int:id>/update", methods=("GET", "POST"))
@login_required
def update(id):
    post = _get_post(id)

    if request.method == "POST":
        view_model = UpdateBlogViewModel(request)
        view_model.load()

        if view_model.error:
            flash(view_model.error)

        else:
            db_session = get_db()
            post.title = view_model.title
            post.body = view_model.body
            db_session.commit()

            return redirect(url_for("blog.index"))

    return render_template("update.jinja", post=post)


@bp.route("/<int:id>/delete", methods=("POST",))
@login_required
def delete(id: int):
    post = _get_post(id)

    db_session = get_db()
    db_session.delete(post)
    db_session.commit()

    return redirect(url_for("index"))
