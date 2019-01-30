from django import forms


class FeedbackValidator(object):
    @staticmethod
    def validate_min_value(rq_data):
        min_value = rq_data.cleaned_data.get('min_value')
        max_value = rq_data.cleaned_data.get('max_value')
        if min_value > max_value:
            rq_data.add_error('min_value', 'Min value must be less then max value')
        return min_value
