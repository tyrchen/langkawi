from django.core.urlresolvers import reverse
from langkawi.contrib.linkedin.client import LinkedIn
from langkawi.contrib.linkedin.models import LinkedInProfile
from langkawi.views import OAuthRedirect, OAuthCallback, SetupCallback

class LinkedInRedirect(OAuthRedirect):
    client = LinkedIn
    template_name = 'langkawi/linkedin/linkedin.html'

class LinkedInCallback(OAuthCallback):
    client = LinkedIn
    template_name = 'langkawi/linkedin/linkedin.html'
    
    def get_redirect(self):
        return reverse('langkawi:linkedin:setup')

class LinkedInSetup(SetupCallback):
    client = LinkedIn
    profile = LinkedInProfile
    template_name = 'langkawi/linkedin/linkedin.html'
    
    def get_lookup_kwargs(self, request, client):
        return {'linkedin_id': client.get_user_info()['id']}
    
