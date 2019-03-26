from django.contrib.sessions.models import Session
from django.db import transaction

from CultureAnalyzer.utils import login_redirect

__all__ = ['AuthRequiredMiddleware', 'SwitchSessionDataMiddleware']


class AuthRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    @login_redirect
    def __call__(self, request):
        return self.get_response(request)


class SwitchSessionDataMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        self._check_session(request)

        return self.get_response(request)

    @transaction.atomic()
    def _check_session(self, request):
        """
        Method, which checks if there previous session, that`s mean has changed
         the client from which user authenticated.

        :var current_session_key(str): hashed key, which identifies current
         session;
        :var stored_session_key(str): hashed key, which identifies previous
         session;
        """
        if request.user.is_authenticated:
            current_session_key = request.session.session_key
            stored_session_key = request.user.logged_in_user.session_key

            if stored_session_key and stored_session_key != current_session_key:
                self.switch_session_data(request, current_session_key,
                                         stored_session_key)

            # update LoggedInUser table with relevant session key
            request.user.logged_in_user.session_key = current_session_key
            request.user.logged_in_user.save()

    @staticmethod
    def switch_session_data(request, current_session_key,
                            stored_session_key):
        """
        Method, which get data from previous session, remove it
        (previous session) and set this data to current session.
        :param request;
        :param current_session_key: hashed key, which identifies current
         session;
        :param stored_session_key: hashed key, which identifies previous
         session;
        :var stored_session_data(str): hashed data from previous session;
        :var expire_date(datetime): future date, which means when the session
         becomes inactive.
        """
        # getting previous session data
        stored_session_data = Session.objects.get(
            session_key=stored_session_key).session_data
        # remove not used anymore session
        Session.objects.get(session_key=stored_session_key).delete()

        expire_date = request.session.get_expiry_date()

        # update current session
        session_object = Session.objects.get(session_key=current_session_key)
        session_object.session_data = stored_session_data
        session_object.expire_date = expire_date
        session_object.save()
