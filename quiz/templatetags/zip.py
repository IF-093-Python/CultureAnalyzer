from django.template import Library

register = Library()


@register.filter(name='zip')
def zip_list(a, b):
    return zip(a, b)
