class CAError(Exception):
    pass


class FValidationError(CAError, ValueError):
    pass
