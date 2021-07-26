from __future__ import annotations

import datetime
import logging
from dataclasses import dataclass
from typing import List

from flask import Request

from flask_blog.orm import db
from flask_blog.services import blog_post_service
from flask_blog.view_models.viewmodel_base import ViewModelBase

_LOGGER = logging.getLogger(__name__)


@dataclass
class BlogPost:
    id: int | None = None
    title: str | None = None
    body: str | None = None
    created: datetime.datetime | None = None
    author_id: int | None = None
    username: str | None = None


class IndexViewModel(ViewModelBase):
    def __init__(self, request: Request) -> None:
        super().__init__(request)
        self.posts: List[BlogPost] = []

    def load(self):
        _LOGGER.info("Loading index view model")
        session = db.get_db()
        try:
            posts = blog_post_service.latest_posts(session)

            # Perform this while the session is active.
            # If session is closed it will raise an error.
            for post in posts:
                self.posts.append(
                    BlogPost(
                        id=post.id,
                        title=post.title,
                        body=post.body,
                        created=post.created,
                        author_id=post.author_id,
                        username=post.author.username,
                    )
                )

        finally:
            session.close()
