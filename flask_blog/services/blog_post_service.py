"""Blog posts related service."""

from __future__ import annotations

import logging
from typing import List

from sqlalchemy.orm.session import Session
from sqlalchemy.sql.expression import select

from flask_blog.orm.db import get_db
from flask_blog.orm.post import Post

_LOGGER = logging.getLogger(__name__)


def latest_posts(session: Session, limit: int = 5) -> List[Post]:
    query = select(Post).order_by(Post.created.desc()).limit(limit)
    result = session.execute(query).scalars().all()
    _LOGGER.info("Result: %s", result)
    return result


def create_post(title: str, body: str, author_id: int):
    """Create a new blog post."""
    session = get_db()
    post = Post(title, body, author_id)
    session.add(post)


def get_post(id: int) -> Post | None:
    session = get_db()
    query = select(Post).filter(Post.id == id)

    post = session.execute(query).scalar_one_or_none()
    return post
