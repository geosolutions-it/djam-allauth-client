from allauth.socialaccount.providers.base import ProviderAccount
from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


social_config = getattr(
    settings, 'SOCIALACCOUNT_PROVIDERS', {}).get('djam', {})

DJAM_DOMAIN = social_config.get('DJAM_DOMAIN')
DJAM_DOMAIN_SCHEMA = social_config.get('DJAM_DOMAIN_SCHEMA')
DJAM_OPENID_PREFIX = social_config.get('DJAM_OPENID_PREFIX')
DJAM_PROVIDER_NAME = social_config.get('DJAM_PROVIDER_NAME')
DJAM_SESSION_COOKIE_NAME = social_config.get('DJAM_SESSION_COOKIE_NAME')
DJAM_AUTO_LOGOUT = social_config.get('DJAM_AUTO_LOGOUT')
DJAM_SESSION_TOKEN_COOKIE = 'djam_stk'


if not DJAM_DOMAIN:
    raise ImproperlyConfigured('DJAM_DOMAIN is missing in env vars')
if not DJAM_DOMAIN_SCHEMA:
    raise ImproperlyConfigured('DJAM_DOMAIN_SCHEMA is missing in env vars')
if not DJAM_OPENID_PREFIX:
    raise ImproperlyConfigured('DJAM_OPENID_PREFIX is missing in env vars')
if not DJAM_OPENID_PREFIX:
    raise ImproperlyConfigured('DJAM_OPENID_PREFIX is missing in env vars')
if not DJAM_SESSION_COOKIE_NAME:
    raise ImproperlyConfigured('DJAM_SESSION_COOKIE_NAME is missing in env vars')
if DJAM_AUTO_LOGOUT is None:
    raise ImproperlyConfigured('DJAM_AUTO_LOGOUT is missing in env vars')


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
            last_name=data['family_name'],
            first_name=data['given_name']
        )

    def extract_user_claims(self, data):
        return {
            'groups': data.get('groups', [])
        }

    def get_default_scope(self):
        scope = ['openid', 'profile', 'user_id', 'groups', 'legacy_user_id']
        return scope


provider_classes = [DjamProvider]
