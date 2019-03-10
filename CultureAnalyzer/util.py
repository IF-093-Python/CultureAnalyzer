from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponseRedirect
from django.urls import reverse

from CultureAnalyzer.settings import REDIRECT_EXCLUDE_ROUTES, LOGIN_URL

__all__ = ['login_redirect']


def not_need_login_redirect(request) -> bool:
    is_user_authenticated = request.user.is_authenticated
    is_exclude_route = any(request.path.startswith(f'/{r}/')
                           for r in REDIRECT_EXCLUDE_ROUTES)
    return is_user_authenticated or is_exclude_route


def get_request(*args) -> WSGIRequest:
    return next((r for r in args if isinstance(r, WSGIRequest)), None)


def login_redirect(get_response):
    def wrapper(*args):
        request, response = get_request(*args), get_response(*args)
        if not_need_login_redirect(request):
            return response
        return HttpResponseRedirect(reverse(LOGIN_URL))

    return wrapper
