# djam-allauth-client
Django Allauth provider for Djam

This library have to be used in complete geonode environment. It uses allauth and django tools but does not provide them as dependencies.

DJAM_DOMAIN = social_config.get('DJAM_DOMAIN', 'localhost:8800')
DJAM_DOMAIN_SCHEMA = social_config.get('DJAM_DOMAIN', 'http')
DJAM_OPENID_PREFIX = social_config.get('DJAM_DOMAIN', 'openid')
DJAM_PROVIDER_NAME = social_config.get('DJAM_DOMAIN', 'Mapstand signin service')
DJAM_SESSION_COOKIE_NAME = social_config.get('DJAM_DOMAIN', 'oauth2server_sessionid')

To incorporate it in geonode:
 - specyfi package in installed apps 
 - specify djam entry in SOCIALACCOUNT_PROVIDERS:
    {.
     .
        'djam': { 'DJAM_DOMAIN':'', 'DJAM_DOMAIN_SCHEMA':'', 'DJAM_OPENID_PREFIX':'','DJAM_PROVIDER_NAME':'','DJAM_SESSION_COOKIE_NAME':'' }
     .
     .
    }
 - Override allauth/logout.html template using one from lib
 - add djam_urlpatterns to geonode urls
 - add `'%s/djamauthprovider/*' % FORCE_SCRIPT_NAME` line to `AUTH_EXEMPT_URLS`