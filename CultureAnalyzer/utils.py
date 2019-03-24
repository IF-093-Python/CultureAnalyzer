from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponseRedirect as Redirect

from CultureAnalyzer.settings import REDIRECT_EXCLUDE_ROUTES, LOGIN_URL

__all__ = ['login_redirect']


def is_exclude_route(request: WSGIRequest) -> bool:
    return any(request.path.startswith(f'/{r}/')
               for r in REDIRECT_EXCLUDE_ROUTES)


def not_need_login_redirect(request: WSGIRequest) -> bool:
    return request.user.is_authenticated or is_exclude_route(request)


def get_request(*args) -> WSGIRequest:
    return next((r for r in args if isinstance(r, WSGIRequest)), None)


def login_page_url(next_page, login_url=LOGIN_URL) -> str:
    return f'/{login_url}/?next={next_page}'


def login_redirect(get_response):
    def wrapper(*args):
        request = get_request(*args)
        if not_need_login_redirect(request):
            return get_response(*args)
        return Redirect(login_page_url(next_page=request.path))

    return wrapper
