class BaseException(Exception):
    message: str = "Internal Server Error"

    def __init__(self, message: str | None = None):
        if message:
            self.message = message


class NotFoundExcepition(BaseException):
    message = "Not Found"

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
