import requests
import logging

from djam_allauth_client.provider import DjamProvider
from djam_allauth_client import provider

from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.providers.oauth2.views import OAuth2Adapter
from allauth.socialaccount.models import SocialAccount

from django.conf import settings
from django.contrib.auth import get_user_model


logger = logging.getLogger(__name__)


class SocialAccountException(Exception):
    pass


class AccountSocialAdapter(DefaultSocialAccountAdapter):

    def is_auto_signup_allowed(self, request, sociallogin):
        """
        This is potentially dangerous.
        It is created to skipp additinal request to create user during first remote user login
        """
        return True

    def populate_user(self,
                      request,
                      sociallogin,
                      data):
        user = super(AccountSocialAdapter, self).populate_user(
            request, sociallogin, data)
        user.last_name = data.get('last_name')
        user.first_name = data.get('first_name')
        user.is_superuser = data.get('is_admin')
        user.is_staff = data.get('is_staff')

        # above user variable will be persisted only if its new.
        # so its not enough to update user data on each login.
        # _update_existing_user will force update
        self._update_existing_user(sociallogin, data)
        return user

    def _update_existing_user(self, sociallogin, data):
        try:
            a = SocialAccount.objects.get(uid=sociallogin.account.uid)
            a.user.last_name = data.get('last_name')
            a.user.first_name = data.get('first_name')
            a.user.email = data.get('email')
            a.user.save()
        except SocialAccount.DoesNotExist:
            pass

    def authentication_error(self,
                             request,
                             provider_id,
                             error=None,
                             exception=None,
                             extra_context=None):
        raise SocialAccountException(exception) from exception


    def new_user(self, request, sociallogin):
        username = sociallogin.account.extra_data.get('nickname')
        UserModel = get_user_model()
        return UserModel(username=username)

    def save_user(self, request, sociallogin, form=None):
        """
        Creates new user instance, or match existing one with social account and invalidate password
        """
        UserModel = get_user_model()
        user_id = sociallogin.account.extra_data.get('legacy_user_id')
        match_legacy_users = getattr(settings, 'DJAM_MATCH_LEGACY_USERS', False)
        if match_legacy_users:
            try:
                legacy_user = UserModel.objects.get(pk=user_id)
                legacy_user.set_unusable_password()
                return sociallogin.connect(request, legacy_user)
            except UserModel.DoesNotExist:
                return super(AccountSocialAdapter, self).save_user(request, sociallogin)
        else:
            return super(AccountSocialAdapter, self).save_user(request, sociallogin)


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
        p = self.get_provider()
        request.session['claims'] = p.extract_user_claims(extra_data)
        sociallogin = self.get_provider().sociallogin_from_response(
            request,
            extra_data
        )
        return sociallogin
