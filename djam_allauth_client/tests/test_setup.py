from django.test import TestCase, override_settings
from djam_allauth_client import provider

domain = 'the_domain'
schema = 'https'
prefix = 'prefix'
name = 'the name'
cookie = 'cooke_name'


class TestClientSetup(TestCase):

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
        self.assertEqual(provider.DJAM_DOMAIN, domain)
        self.assertEqual(provider.DJAM_DOMAIN_SCHEMA, schema)
        self.assertEqual(provider.DJAM_OPENID_PREFIX, prefix)
        self.assertEqual(provider.DJAM_SESSION_COOKIE_NAME, cookie)
        self.assertEqual(provider.DJAM_PROVIDER_NAME, name)
