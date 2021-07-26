from __future__ import annotations

from flask_blog.view_models.viewmodel_base import ViewModelBase


class CreateBlogViewModel(ViewModelBase):
    title: str | None = None
    body: str | None = None

    def load(self):
        self.title = self.request.form.get("title")
        self.body = self.request.form.get("body")

        if not self.title:
            self.error = "Title is required."
        elif not self.body:
            self.error = "Post content is required."


class UpdateBlogViewModel(ViewModelBase):
    title: str | None = None
    body: str | None = None

    def load(self):
        self.title = self.request.form.get("title")
        self.body = self.request.form.get("body")

        if not self.title:
            self.error = "Title is required."
