from allauth.socialaccount.providers.oauth2.urls import default_urlpatterns
from django.conf.urls import url

from djam_allauth_client.providers import DjamProvider
from djam_allauth_client.views import DjamSignupView

djam_urlpatterns = default_urlpatterns(DjamProvider)
djam_urlpatterns += [url('account/signup', DjamSignupView.as_view(), name='djam_register')]