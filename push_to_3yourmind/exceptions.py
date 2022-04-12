class BasePushTo3YourmindAPIException(Exception):
    """
    Base exception class for all exceptions raised by push_to_3yourmind
    """


class ObjectNotFound(BasePushTo3YourmindAPIException):
    pass


class Unauthorized(BasePushTo3YourmindAPIException):
    pass


class AccessDenied(BasePushTo3YourmindAPIException):
    pass


class BadRequest(BasePushTo3YourmindAPIException):
    pass


class MethodNotAllowed(BasePushTo3YourmindAPIException):
    pass


class ServerError(BasePushTo3YourmindAPIException):
    pass


class BadArgument(BasePushTo3YourmindAPIException):
    pass


class MaterialNotFound(BasePushTo3YourmindAPIException):
    pass


class PostProcessingNotFound(BasePushTo3YourmindAPIException):
    pass


class SupplierNotFound(BasePushTo3YourmindAPIException):
    pass


class FileAnalysisError(BasePushTo3YourmindAPIException):
    pass


class CADFileNotFoundError(BasePushTo3YourmindAPIException):
    pass

