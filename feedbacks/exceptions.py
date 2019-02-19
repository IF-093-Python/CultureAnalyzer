__all__ = ['FValidationError', ]


class CAError(Exception):
    pass


class FValidationError(CAError, ValueError):
    pass
