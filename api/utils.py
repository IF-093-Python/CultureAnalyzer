from typing import Tuple, Any


def first_hit_value(conditions: Tuple[bool],
                    return_conditions: Tuple[Any],
                    default: Any = None) -> Any:
    """ Can be used only for small data sets """
    return next((return_conditions[i] for i, c in enumerate(conditions) if c),
                default)
