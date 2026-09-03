class NotFoundError(Exception):
    """Raised when a requested resource does not exist. Maps to HTTP 404."""


class ValidationError(Exception):
    """Raised for invalid request data or constraint violations. Maps to HTTP 422."""

    def __init__(self, errors: list[dict[str, str]]):
        self.errors = errors
        super().__init__(str(errors))


def field_error(field: str, message: str) -> ValidationError:
    return ValidationError([{"field": field, "message": message}])
