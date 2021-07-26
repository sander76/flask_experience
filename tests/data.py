"""Data to be used during testing.

In a previous version I did not use the `get` functions to return
orm model instances. I used `USERS` or `POSTS` instead which were lists
containing these instances.

```
USERS = [User(username("Gullich",pass="pass"))]
```

However if you start testing you want to recreate the database on each run.
And you cannot re-use these USERS across different databases.

"""

from typing import List

from werkzeug.security import generate_password_hash

from flask_blog.orm.db import get_db
from flask_blog.orm.modelbase import SqlAlchemyBase
from flask_blog.orm.post import Post
from flask_blog.orm.user import User


def get_posts():
    return [
        Post(
            title="the title",
            body="this is the contents of the blog post.",
            author_id=1,
        ),
        Post(
            title="Into the void", body="This is the contexts of the void.", author_id=2
        ),
    ]


def get_users():
    return [
        User(username="Güllich", password=generate_password_hash("action")),
        User(username="Graham", password=generate_password_hash("the island")),
    ]


def add_data(*orm_models: List[SqlAlchemyBase]):
    session = get_db()

    # try:
    for model in orm_models:
        for obj in model:
            session.add(obj)
    session.commit()
