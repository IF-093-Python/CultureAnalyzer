from django.http import HttpResponseRedirect
from django.urls import reverse

__all__ = ['AuthRequiredMiddleware']


def not_need_login_redirect(request) -> bool:
    is_user_authenticated = request.user.is_authenticated
    is_login_page = request.path.startswith('/login/')
    return is_user_authenticated or is_login_page


class AuthRequiredMiddleware:
    def __init__(self, response):
        self.get_response = response

    def __call__(self, request):
        if not_need_login_redirect(request):
            return self.get_response(request)
        return HttpResponseRedirect(reverse('login'))
