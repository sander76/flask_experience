"""A blog post orm."""
import datetime

import sqlalchemy as sa
from sqlalchemy import orm

from flask_blog.orm.modelbase import SqlAlchemyBase
from flask_blog.orm.user import User


class Post(SqlAlchemyBase):
    __tablename__ = "post"

    id: int = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    author_id: int = sa.Column(sa.Integer, sa.ForeignKey("user.id"))
    author: User = orm.relation("User")  # I've seen this somewhere. Is this usable ?

    created: datetime.datetime = sa.Column(sa.DateTime, default=datetime.datetime.now)
    title: str = sa.Column(sa.String, nullable=False)
    body: str = sa.Column(sa.String, nullable=False)

    def __init__(self, title: str, body: str, author_id: int):
        self.title = title
        self.body = body
        self.author_id = author_id
