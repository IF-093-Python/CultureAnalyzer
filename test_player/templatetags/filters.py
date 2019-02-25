from django.template import Library

register = Library()


@register.filter(name='lookup')
def lookup(value, arg):
    """
    Filter for retrive value from dict.

    :param dict_container: dict
    :param key: string or key which possible convert to string
    :return: value from dict_container, return False if value is not found
    """
    if value:
        return value.get(str(arg), False)
