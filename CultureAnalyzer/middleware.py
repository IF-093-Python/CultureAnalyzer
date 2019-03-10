from CultureAnalyzer.util import login_redirect

__all__ = ['AuthRequiredMiddleware']


class AuthRequiredMiddleware:
    def __init__(self, response):
        self.get_response = response

    @login_redirect
    def __call__(self, request):
        return self.get_response(request)
