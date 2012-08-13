from django.core.urlresolvers import reverse
from langkawi.contrib.twitter.client import Twitter
from langkawi.contrib.twitter.models import TwitterProfile
from langkawi.views import OAuthRedirect, OAuthCallback, SetupCallback

class TwitterRedirect(OAuthRedirect):
    client = Twitter
    template_name = 'langkawi/twitter/twitter.html'

class TwitterCallback(OAuthCallback):
    client = Twitter
    template_name = 'langkawi/twitter/twitter.html'
    
    def get_redirect(self):
        return reverse('langkawi:twitter:setup')

class TwitterSetup(SetupCallback):
    client = Twitter
    profile = TwitterProfile
    template_name = 'langkawi/twitter/twitter.html'
    
    def get_lookup_kwargs(self, request, client):
        return {'twitter_id': client.get_user_info()['user_id']}
    
