from django.shortcuts import redirect
from django.views import View
from django.conf import settings
from allauth.socialaccount.providers.oauth2.views import OAuth2CallbackView, OAuth2LoginView
from djam_allauth_client.adapters import DjamAdapter


class DjamSignupView(View):

    def get(self, request, *args, **kwargs):
        return redirect('{}://{}/register'.format(settings.DJAM_DOMAIN_SCHEMA, settings.DJAM_DOMAIN))


oauth2_login = OAuth2LoginView.adapter_view(DjamAdapter)
oauth2_callback = OAuth2CallbackView.adapter_view(DjamAdapter)