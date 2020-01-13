import imp
from django.test import TestCase, override_settings, RequestFactory
from djam_allauth_client import provider
from djam_allauth_client import adapters
from allauth.account.models import EmailAddress
from django.contrib.sessions.middleware import SessionMiddleware
import mock

domain = 'the_domain'
schema = 'https'
prefix = 'prefix'
name = 'the name'
cookie = 'cooke_name'


class MockResponse():
    def __init__(self, v):
        self.v = v

    def json(self):
        return self.v


def build_mock_response(*args, **kwargs):
    return MockResponse({
        'user_id': 1,
        'nickname': 'test_name',
        'sub': '1',
        'email': 'test@test.com'
    })


class TestClientSetup(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    @override_settings(SOCIALACCOUNT_PROVIDERS={
        'djam': {
            'DJAM_DOMAIN': domain,
            'DJAM_DOMAIN_SCHEMA': schema,
            'DJAM_OPENID_PREFIX': prefix,
            'DJAM_PROVIDER_NAME': name,
            'DJAM_SESSION_COOKIE_NAME': cookie
        }
    })
    def test_configuration_setup(self):
        # hack to reload module after settings are faked
        imp.reload(provider)
        self.assertEqual(provider.DJAM_DOMAIN, domain)
        self.assertEqual(provider.DJAM_DOMAIN_SCHEMA, schema)
        self.assertEqual(provider.DJAM_OPENID_PREFIX, prefix)
        self.assertEqual(provider.DJAM_SESSION_COOKIE_NAME, cookie)
        self.assertEqual(provider.DJAM_PROVIDER_NAME, name)

    def test_djam_scope(self):
        djam_scope = ['openid', 'email', 'profile', 'user_id']
        p = provider.DjamProvider(self.factory.get('account/login?next=/'))
        sc = p.get_default_scope()
        self.assertEqual(djam_scope, sc)

    def test_data_extraction(self):
        data = {
            'user_id': 1,
            'nickname': 'test_name',
            'sub': '1',
            'email': 'test@test.com'
        }

        p = provider.DjamProvider(self.factory.get('account/login?next=/'))
        uid = p.extract_uid(data)
        self.assertEqual(data.get('user_id'), uid)

        email_list = [[EmailAddress(email=data.get('email'),
                                    verified=True,
                                    primary=True)]]
        p.extract_email_addresses(data)
        self.assertEqual(data.get('user_id'), uid)

        fields = {
            'username': data.get('nickname'),
            'email': data.get('email'),
        }

        f = p.extract_common_fields(data)
        self.assertEqual(f, fields)

    @mock.patch('requests.get', side_effect=build_mock_response)
    def test_session_update(self, mock_requests):
        data = {
            'user_id': 1,
            'nickname': 'test_name',
            'sub': '1',
            'email': 'test@test.com'
        }
        r = self.factory.get(
            '/djamauthprovider/login/callback/?code=unrelevant_value&state=unrelevant_value')

        middleware = SessionMiddleware()
        middleware.process_request(r)
        r.session.save()

        response = {
            u'access_token': u'unrelevant_value',
            u'token_type': u'bearer',
            u'expires_in': 3600,
            u'refresh_token': u'unrelevant_value',
            u'id_token': u'unrelevant_value'}
        a = adapters.DjamAdapter(r)
        token = a.parse_token({'access_token': 'unrelevant_value'})
        sl = a.complete_login(r, None, token, response=response)

        self.assertTrue(r.session.get('id_token') is not None)
        self.assertEqual(sl.user.username, data.get('nickname'))
