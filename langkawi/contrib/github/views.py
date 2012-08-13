from django.core.urlresolvers import reverse
from langkawi.contrib.github.client import Github
from langkawi.contrib.github.models import GithubProfile
from langkawi.views import OAuthRedirect, OAuthCallback, SetupCallback

class GithubRedirect(OAuthRedirect):
    client = Github
    template_name = 'langkawi/github/github.html'

class GithubCallback(OAuthCallback):
    client = Github
    template_name = 'langkawi/github/github.html'
    
    def get_redirect(self):
        return reverse('langkawi:github:setup')

class GithubSetup(SetupCallback):
    client = Github
    profile = GithubProfile
    template_name = 'langkawi/github/github.html'
    
    def get_lookup_kwargs(self, request, client):
        return {'github': client.get_user_info()['login']}
    
