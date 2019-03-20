__all__ = ['FValidationError', 'PValidationError']


class CAError(Exception):
    pass


class FValidationError(CAError, ValueError):
    pass


class PValidationError(CAError, ValueError):
    pass
