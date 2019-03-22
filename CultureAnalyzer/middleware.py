from CultureAnalyzer.util import login_redirect
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.models import Session

__all__ = ['AuthRequiredMiddleware', 'SwitchSessionDataMiddleware']


class AuthRequiredMiddleware:
    def __init__(self, response):
        self.get_response = response

    @login_redirect
    def __call__(self, request):
        return self.get_response(request)


class SwitchSessionDataMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        if request.user.is_authenticated:
            stored_session_key = request.user.logged_in_user.session_key

            if stored_session_key and stored_session_key != request.session.session_key:
                stored_session_data = Session.objects.get(
                    session_key=stored_session_key).get_decoded()
                expire_date = request.session.get_expiry_date()
                encoded_data = SessionStore().encode(stored_session_data)
                Session.objects.get(session_key=stored_session_key).delete()
                Session.objects.update(
                    session_key=request.session.session_key,
                    session_data=encoded_data, expire_date=expire_date)

            request.user.logged_in_user.session_key = request.session.session_key
            request.user.logged_in_user.save()

        response = self.get_response(request)

        return response
