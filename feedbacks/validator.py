from CultureAnalyzer.exceptions import FValidationError

__all__ = ['FeedbackValidator', ]


class FeedbackValidator:
    @staticmethod
    def validate_min_value(rq_data):
        if rq_data.get('min_value') >= rq_data.get('max_value'):
            raise FValidationError('Min value must be less then max value')
