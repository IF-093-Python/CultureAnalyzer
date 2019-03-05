from datetime import date

__all__ = ['ProfileValidator', 'PValidationError']

MIN_YEARS_OF_EXPERIENCE = 0
MAX_YEARS_OF_EXPERIENCE = 100


class CAError(Exception):
    pass


class PValidationError(CAError, ValueError):
    pass


class ProfileValidator:
    @staticmethod
    def validate(rq_data):
        experience = rq_data.get('experience')

        if not isinstance(experience, int):
            raise PValidationError('Only integer values are supported')

        elif not MIN_YEARS_OF_EXPERIENCE < experience < MAX_YEARS_OF_EXPERIENCE:
            raise PValidationError(
                f'Enter correct data (from {MIN_YEARS_OF_EXPERIENCE} to'
                f' {MAX_YEARS_OF_EXPERIENCE})')

        return experience

    @staticmethod
    def date_validation(rq_data):
        date_of_birth = rq_data.get('date_of_birth')
        difference = (date.today() - date_of_birth).days / 365.2425

        if difference < 18:
            raise PValidationError('You should be at least 18 year old!')
        return date_of_birth
