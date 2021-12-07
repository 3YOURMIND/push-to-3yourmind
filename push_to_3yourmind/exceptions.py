class BasePushTo3YourmindAPIException(Exception):
    pass


class ObjectNotFound(BasePushTo3YourmindAPIException):
    pass


class Unauthorized(BasePushTo3YourmindAPIException):
    pass


class BadRequest(BasePushTo3YourmindAPIException):
    pass


class MethodNotAllowed(BasePushTo3YourmindAPIException):
    pass


class ServerError(BasePushTo3YourmindAPIException):
    pass


class BadArgument(BasePushTo3YourmindAPIException):
    pass
