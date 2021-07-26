import sqlalchemy as sa

from flask_blog.orm.modelbase import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = "user"

    id: int = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    username = sa.Column(sa.String, unique=True, nullable=False)
    password = sa.Column(sa.String, nullable=False)
