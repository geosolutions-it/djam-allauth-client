from allauth.socialaccount.providers.oauth2.urls import default_urlpatterns
from djam_allauth_client.views import djam_logout
from django.conf.urls import url

from djam_allauth_client.provider import DjamProvider

djam_urlpatterns = default_urlpatterns(DjamProvider)
djam_urlpatterns += [url('account/djamlogout', djam_logout, name='djam_logout')]
