from allauth.account.models import EmailAddress
from allauth.socialaccount.providers.base import ProviderAccount
from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider
from django.conf import settings


social_config = getattr(
    settings, 'SOCIALACCOUNT_PROVIDERS', {}).get('djam', {})

DJAM_DOMAIN = social_config.get('DJAM_DOMAIN', 'localhost:8800')
DJAM_DOMAIN_SCHEMA = social_config.get('DJAM_DOMAIN', 'http')
DJAM_OPENID_PREFIX = social_config.get('DJAM_DOMAIN', 'openid')
DJAM_PROVIDER_NAME = social_config.get('DJAM_DOMAIN', 'Mapstand signin service')
DJAM_SESSION_COOKIE_NAME = social_config.get('DJAM_DOMAIN', 'oauth2server_sessionid')


class DjamAccount(ProviderAccount):
    pass


class DjamProvider(OAuth2Provider):
    id = 'djamauthprovider'
    name = DJAM_PROVIDER_NAME
    account_class = DjamAccount

    def extract_uid(self, data):
        return data.get('user_id')

    def extract_email_addresses(self, data):
        return [EmailAddress(email=data['email'],
                             verified=True,
                             primary=True)]

    def extract_common_fields(self, data):
        return dict(
            username=data['nickname'],
            email=data['email'],
        )

    def get_default_scope(self):
        scope = ['openid', 'email', 'profile', 'user_id']
        return scope


provider_classes = [DjamProvider]

