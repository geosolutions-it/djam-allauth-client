import requests
from allauth.account.views import LogoutView as AllauthLogout
from allauth.exceptions import ImmediateHttpResponse
from allauth.socialaccount.providers.oauth2.views import OAuth2CallbackView, OAuth2LoginView
from djam_allauth_client.adapters import DjamAdapter
from django.shortcuts import redirect, render
from django.http import HttpResponseServerError, HttpResponseRedirect
from rest_framework import status
from allauth.socialaccount import providers


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

    def post(self, *args, **kwargs):
        request = args[0]
        id_token = request.session.get('id_token')
        if id_token:
            r = requests.get('{}/?id_token_hint={}'.format(self.adapter.end_sesion, id_token))
            if r.status_code == status.HTTP_200_OK:
                response = super(DjamLogoutView, self).post(*args, **kwargs)
                if response.status_code == status.HTTP_302_FOUND:
                    r = HttpResponseRedirect(r.url)
                    r.delete_cookie('oauth2server_sessionid')
                    return r
                else:
                    return response
        else:
            return render(request, '500.html', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

oauth2_login = OAuth2LoginView.adapter_view(DjamAdapter)
oauth2_callback = OAuth2CallbackView.adapter_view(DjamAdapter)
djam_logout = DjamLogoutView.adapter_view(DjamAdapter)

providers.registry.register(DjamProvider)