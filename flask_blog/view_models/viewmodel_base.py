from typing import Optional

from flask import Request


class ViewModelBase:
    error: Optional[str] = None

    def __init__(self, request: Request) -> None:
        self.request = request

        # todo: manage this through an auth cookie.
        self.user_id: Optional[int] = None

        self.is_logged_id = self.user_id is not None

    def to_dict(self) -> dict:
        return self.__dict__
