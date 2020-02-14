import requests
from allauth.account.views import LogoutView as AllauthLogout
from allauth.exceptions import ImmediateHttpResponse
from allauth.socialaccount.providers.oauth2.views import OAuth2CallbackView, OAuth2LoginView
from djam_allauth_client.adapters import DjamAdapter
from django.shortcuts import redirect, render
from django.http import HttpResponseServerError, HttpResponseRedirect
from rest_framework import status
from django.conf import settings

from djam_allauth_client.provider import DJAM_SESSION_COOKIE_NAME, DJAM_SESSION_TOKEN_COOKIE


class DjamCallbackView(OAuth2CallbackView):

    def dispatch(self, request, *args, **kwargs):
        response = super(DjamCallbackView, self).dispatch(request, *args, **kwargs)
        response.set_cookie(DJAM_SESSION_TOKEN_COOKIE,value= request.session.get('session_token'))
        return response


class DjamLogoutView(AllauthLogout):

    @classmethod
    def adapter_view(cls, adapter):
        def view(request, *args, **kwargs):
            self = cls()
            self.request = request
            self.adapter = adapter(request)
            try:
                return self.dispatch(request, *args, **kwargs)
            except ImmediateHttpResponse as e:
                return e.response

        return view

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

    def post(self, *args, **kwargs):
        request = args[0]
        id_token = request.session.get('id_token')
        if id_token:
            response = super(DjamLogoutView, self).post(*args, **kwargs)
            if response.status_code == status.HTTP_302_FOUND:
                r = HttpResponseRedirect('{}/?id_token_hint={}'.format(self.adapter.end_sesion, id_token))
                r.set_cookie(DJAM_SESSION_TOKEN_COOKIE, max_age=1, value='')
                return r
            else:
                return response
        else:
            return render(request, '500.html', status=status.HTTP_500_INTERNAL_SERVER_ERROR)


oauth2_login = OAuth2LoginView.adapter_view(DjamAdapter)
oauth2_callback = DjamCallbackView.adapter_view(DjamAdapter)
djam_logout = DjamLogoutView.adapter_view(DjamAdapter)
