from django.utils import timezone

from CultureAnalyzer.exceptions import PValidationError

__all__ = ['SheduleValidator', 'InvitationValidator']


class SheduleValidator:
    @staticmethod
    def start_validator(start):
        if start < timezone.now():
            raise PValidationError(
                'Start date already passed! Please enter valid date.')
        return start

    @staticmethod
    def end_validator(start, end):
        if start >= end:
            raise PValidationError('End date should be after start date!')
        return end


class InvitationValidator:
    @staticmethod
    def date_validator(end):
        if end < timezone.now():
            raise PValidationError(
                'End date already passed! Please enter valid date.')
        return end

    @staticmethod
    def items_validator(items):
        if not items:
            raise PValidationError(
                'Input number of students to invite to this group.')
        return items
