__all__ = ['PValidationError', ]


class CAError(Exception):
    pass


class PValidationError(CAError, ValueError):
    pass
