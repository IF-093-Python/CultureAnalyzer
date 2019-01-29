from collections import Iterable


def deep_flatten(field):
    """
    Get items from nested Iterable

    :param Iterable field:
    :return Generator:
    """
    for item in field:
        if isinstance(item, Iterable):
            for x in deep_flatten(item):
                yield x
        else:
            yield item
