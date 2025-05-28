from app.common.exceptions import NotFound


class UserNotFound(NotFound):
    """
    Exception class for 404 User Not Found
    """

    def __init__(self, *, loc: list | None = None):
        super().__init__("User Not Found", loc=loc)
