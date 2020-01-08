from allauth.socialaccount.providers.oauth2.urls import default_urlpatterns
from django.conf.urls import url

from djam_allauth_client.providers import DjamProvider

djam_urlpatterns = default_urlpatterns(DjamProvider)
djam_urlpatterns += [url('account/djamlogout', djam_logout, name='djam_logout')]
