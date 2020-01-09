# djam-allauth-client
Django Allauth provider for Djam

This library have to be used in complete geonode environment. It uses allauth and django tools but does not provide them as dependencies.

To incorporate it in geonode:
 - Import all variables from settings.py to geonode settings (override them there if required)
 - Override allauth/logout.html template using one from lib
 - add djam_urlpatterns to geonode urls
 - add `'%s/djamauthprovider/*' % FORCE_SCRIPT_NAME` line to `AUTH_EXEMPT_URLS`