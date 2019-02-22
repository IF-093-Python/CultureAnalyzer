from django.template import Library

register = Library()


@register.filter(name='lookup')
def lookup(value, arg):
    if value:
        return value.get(str(arg), False)
