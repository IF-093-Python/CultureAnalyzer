from django.utils import timezone


def dates_validator(data):
    errors = {}
    start = data['start']
    end = data['end']
    if data['form'] == 'SheduleForm' and start < timezone.now():
        msg = u'Start date already passed! Please enter valid date.'
        errors['begin'] = msg
    if data['form'] == 'InvitationForm':
        if end < timezone.now():
            msg = u'End date already passed! Please enter valid date.'
            errors['end'] = msg
        if not data['items']:
            msg = u'Input number of students to invite to this group.'
            errors['items_left'] = msg
    if start >= end:
        msg = u'End date should be after start date!'
        errors['end'] = msg
    return errors
