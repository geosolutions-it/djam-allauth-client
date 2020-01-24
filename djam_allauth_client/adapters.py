import requests
from allauth.socialaccount.providers.oauth2.views import OAuth2Adapter
from djam_allauth_client.provider import DjamProvider
from djam_allauth_client import provider


class DjamAdapter(OAuth2Adapter):
    provider_id = DjamProvider.id
    access_token_url = '{}://{}/{}/token'.format(provider.DJAM_DOMAIN_SCHEMA, provider.DJAM_DOMAIN,
                                                 provider.DJAM_OPENID_PREFIX)
    authorize_url = '{}://{}/{}/authorize'.format(provider.DJAM_DOMAIN_SCHEMA, provider.DJAM_DOMAIN,
                                                  provider.DJAM_OPENID_PREFIX)
    profile_url = '{}://{}/{}/userinfo'.format(provider.DJAM_DOMAIN_SCHEMA, provider.DJAM_DOMAIN,
                                               provider.DJAM_OPENID_PREFIX)
    end_sesion = '{}://{}/{}/end-session'.format(provider.DJAM_DOMAIN_SCHEMA, provider.DJAM_DOMAIN,
                                                 provider.DJAM_OPENID_PREFIX)

    def complete_login(self, request, app, token, **kwargs):
        resp = requests.get(self.profile_url, params={
            'access_token': token.token
        })
        request.session['id_token'] = kwargs.get('response', {}).get('id_token')
        request.session['session_token'] = kwargs.get('response', {}).get('session_token')
        extra_data = resp.json()
        return self.get_provider().sociallogin_from_response(
            request,
            extra_data
        )
