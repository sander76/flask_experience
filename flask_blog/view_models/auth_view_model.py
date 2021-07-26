from __future__ import annotations

from werkzeug.security import check_password_hash

from flask_blog.orm import db
from flask_blog.services import user_service
from flask_blog.view_models.viewmodel_base import ViewModelBase


class RegisterViewModel(ViewModelBase):
    name: str | None = None
    password: str | None = None

    def load(self):
        """Load the user form and validate the input."""
        self.name = self.request.form.get("username")
        self.password = self.request.form.get("password")

        session = db.get_db()

        if not self.name or not self.name.strip():
            self.error = "Your name is required."

        elif not self.password or len(self.password) < 5:
            # perform all kinds of password checks here.
            self.error = (
                "Password required or password must be at least 5 characters long."
            )
        elif user_service.get_user_by_name(session, self.name):
            self.error = "User already exists. Login instead?"
        # else:
        #     user_service.create_user(session, self.name, self.password)
        #     return redirect(url_for("auth.login"))

    def create_user(self):
        session = db.get_db()
        user_service.create_user(session, self.name, self.password)


class LoginViewModel(ViewModelBase):
    username: str | None = None
    password: str | None = None

    def load(self):
        self.username = self.request.form.get("username")
        self.password = self.request.form.get("password")

        db_session = db.get_db()

        user = user_service.get_user_by_name(db_session, self.username)
        if user is None:
            self.error = "User does not exist. Register first?"
        elif not check_password_hash(user.password, self.password):
            self.error = "Incorrect password."
