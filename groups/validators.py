from django.utils import timezone


def dates_validator(self, start, end, not_in_past, name, field, items=1):
    if not items:
        msg = u'Input number of students to invite to this group.'
        self.add_error('items_left', msg)
    if not_in_past < timezone.now():
        msg = name.title() + u' date already passed! Please enter valid date.'
        self.add_error(field, msg)
    if start >= end:
        msg = u'End date should be after start date!'
        self.add_error('end', msg)
