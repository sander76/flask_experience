from flask_blog.view_models.index_view_model import IndexViewModel
from tests import data


def test_get_posts_success(app):
    data.add_data(data.get_posts(), data.get_users())
    view_model = IndexViewModel(None)

    view_model.load()

    assert len(view_model.posts) == 2


def test_get_posts_no_posts(app):
    view_model = IndexViewModel(None)

    view_model.load()
    assert len(view_model.posts) == 0


# sqlite+pysqlite:///C:/Users/sander/AppData/Local/Temp/pytest-of-sander/pytest-503/test_get_posts_success0/dbase.sqlite'
# sqlite+pysqlite:///C:/Users/sander/AppData/Local/Temp/pytest-of-sander/pytest-503/test_get_posts_no_posts0/dbase.sqlite
