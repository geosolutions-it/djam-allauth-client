from allauth.socialaccount.providers.oauth2.urls import default_urlpatterns
from djam_allauth_client.views import djam_logout
from django.urls import path

from djam_allauth_client.provider import DjamProvider

urlpatterns = default_urlpatterns(DjamProvider)
urlpatterns += [path('account/djamlogout', djam_logout, name='djam_logout')]
