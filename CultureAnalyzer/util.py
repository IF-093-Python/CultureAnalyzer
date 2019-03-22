from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponseRedirect as Redirect

from CultureAnalyzer.settings import REDIRECT_EXCLUDE_ROUTES, LOGIN_URL

__all__ = ['login_redirect']


def is_exclude_route(request):
    return any(request.path.startswith(f'/{r}/')
               for r in REDIRECT_EXCLUDE_ROUTES)


def not_need_login_redirect(request) -> bool:
    return request.user.is_authenticated or is_exclude_route(request)


def get_request(*args) -> WSGIRequest:
    return next((r for r in args if isinstance(r, WSGIRequest)), None)


def login_page(next_page, login_url=LOGIN_URL):
    return f'/{login_url}/?next={next_page}'


def login_redirect(get_response):
    def wrapper(*args):
        request, response = get_request(*args), get_response(*args)
        if not_need_login_redirect(request):
            return response
        return Redirect(login_page(next_page=request.path))

    return wrapper
