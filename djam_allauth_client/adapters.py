import requests
from allauth.socialaccount.providers.oauth2.views import OAuth2Adapter
from django.conf import settings
from djam_allauth_client.providers import DjamProvider


class DjamAdapter(OAuth2Adapter):
    provider_id = DjamProvider.id
    access_token_url = '{}://{}/{}/token'.format(settings.DJAM_DOMAIN_SCHEMA, settings.DJAM_DOMAIN, settings.DJAM_OPENID_PREFIX)
    authorize_url = '{}://{}/{}/authorize'.format(settings.DJAM_DOMAIN_SCHEMA, settings.DJAM_DOMAIN, settings.DJAM_OPENID_PREFIX)
    profile_url = '{}://{}/{}/userinfo'.format(settings.DJAM_DOMAIN_SCHEMA, settings.DJAM_DOMAIN, settings.DJAM_OPENID_PREFIX)

    def complete_login(self, request, app, token, **kwargs):
        resp = requests.get(self.profile_url, params={
            'access_token': token.token
        })
        extra_data = resp.json()
        return self.get_provider().sociallogin_from_response(
            request,
            extra_data
        )