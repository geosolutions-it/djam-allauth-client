from allauth.account.models import EmailAddress
from allauth.socialaccount.providers.base import ProviderAccount
from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider
from django.conf import settings

social_config = getattr(
    settings, 'SOCIALACCOUNT_PROVIDERS', {}).get('djam', {})

DJAM_DOMAIN = social_config.get('DJAM_DOMAIN', 'localhost:8800')
DJAM_DOMAIN_SCHEMA = social_config.get('DJAM_DOMAIN_SCHEMA', 'http')
DJAM_OPENID_PREFIX = social_config.get('DJAM_OPENID_PREFIX', 'openid')
DJAM_PROVIDER_NAME = social_config.get('DJAM_PROVIDER_NAME', 'Mapstand signin service')
DJAM_SESSION_COOKIE_NAME = social_config.get('DJAM_SESSION_COOKIE_NAME', 'djam_sessionid')
DJAM_SESSION_TOKEN_COOKIE = 'djam_stk'


class DjamAccount(ProviderAccount):
    pass


class DjamProvider(OAuth2Provider):
    id = 'djamauthprovider'
    name = DJAM_PROVIDER_NAME
    account_class = DjamAccount

    def extract_uid(self, data):
        return data.get('user_id')

    def extract_email_addresses(self, data):
        return []

    def extract_common_fields(self, data):
        return dict(
            username=data['nickname'],
        )

    def extract_user_claims(self, data):
        return {
            'groups': data.get('groups', [])
        }

    def get_default_scope(self):
        scope = ['openid', 'profile', 'user_id', 'groups']
        return scope


provider_classes = [DjamProvider]
