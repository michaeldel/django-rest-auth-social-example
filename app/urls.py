import urllib.parse

from allauth.socialaccount.providers.github import views as github_views
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include, path, reverse
from rest_auth.registration.views import SocialLoginView


class GitHubLogin(SocialLoginView):
    adapter_class = github_views.GitHubOAuth2Adapter
    client_class = OAuth2Client

    @property
    def callback_url(self):
        # use the same callback url as defined in your GitHub app, this url must
        # be absolute:
        return self.request.build_absolute_uri(reverse('github_callback'))


def github_callback(request):
    params = urllib.parse.urlencode(request.GET)
    return redirect(f'https://frontend/auth/github?{params}')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('rest_auth.urls')),
    path('', GitHubLogin.as_view()),
    path('auth/github/callback/', github_callback, name='github_callback'),
    path('auth/github/url/', github_views.oauth2_login)
]
