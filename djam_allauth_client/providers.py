from allauth.account.models import EmailAddress
from allauth.socialaccount import providers
from allauth.socialaccount.providers.base import ProviderAccount
from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider
from django.conf import settings

class DjamAccount(ProviderAccount):
    pass


class DjamProvider(OAuth2Provider):
    id = 'djamauthprovider'
    name = settings.DJAM_PROVIDER_NAME
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



providers.registry.register(DjamProvider)
