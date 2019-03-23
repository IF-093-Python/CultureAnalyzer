from django.contrib.sessions.models import Session
from django.db import transaction

from CultureAnalyzer.util import login_redirect

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
                self._switch_session_data(request, current_session_key,
                                          stored_session_key)

    @transaction.atomic()
    def _switch_session_data(self, request, current_session_key,
                             stored_session_key):
        """
        Method, which get data from previous session, remove it
        (previous session) and set this data to current session.

        :param stored_session_key: hashed key, which identifies previous
         session;
        :var current_session_key(str): hashed key, which identifies current
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
        # update current session
        expire_date = request.session.get_expiry_date()
        Session.objects.update(
            session_key=current_session_key,
            session_data=stored_session_data,
            expire_date=expire_date)
        # update LoggedInUser table with relevant session key
        request.user.logged_in_user.session_key = current_session_key
        request.user.logged_in_user.save()
