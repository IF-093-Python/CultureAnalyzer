from django import forms

MIN_YEARS_OF_EXPERIENCE = 0
MAX_YEARS_OF_EXPERIENCE = 100


class ProfileValidator:
    @staticmethod
    def validate_experience(rq_data):
        experience = rq_data.get('experience')

        if not isinstance(experience, int):
            raise forms.ValidationError('Enter correct data')

        elif not MIN_YEARS_OF_EXPERIENCE < experience < MAX_YEARS_OF_EXPERIENCE:
            raise forms.ValidationError(
                f'Enter correct data (from {MIN_YEARS_OF_EXPERIENCE} to'
                f' {MAX_YEARS_OF_EXPERIENCE})')

        return experience
