from typing import Tuple, Any

from api.permissions import is_superadmin, is_admin, is_mentor, is_trainee
from users.models import CustomUser


def get_by_role(user: CustomUser, return_values: Tuple[Any], default=None):
    return first_hit_value(conditions=(is_superadmin(user), is_admin(user),
                                       is_mentor(user), is_trainee(user)),
                           return_values=return_values,
                           default=default)


def first_hit_value(conditions: Tuple[bool],
                    return_values: Tuple[Any],
                    default: Any = None) -> Any:
    """ Can be used only for small data sets """
    return next((return_values[i] for i, c in enumerate(conditions) if c),
                default)
