__all__ = ['FValidationError', 'PValidationError']


class CAError(Exception):
    """Custom parent exception"""
    pass


class FValidationError(CAError, ValueError):
    """Feedback validation has some errors"""
    pass


class PValidationError(CAError, ValueError):
    """Profile validation has some errors"""
    pass
