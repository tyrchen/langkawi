from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import TestCase
from langkawi.contrib.twitter.models import TwitterProfile
from langkawi.tests import TemplateTagTest, OAuthTest
import urllib


class TestTemplateTag(TemplateTagTest, TestCase):
    def get_tag(self):
        return 'twitter', 'twitter_button'

class TestTwitter(OAuthTest, TestCase):
    profile = TwitterProfile

    def get_redirect_url(self):
        return reverse('langkawi:twitter:redirect')
    
    def get_callback_url(self):
        return reverse('langkawi:twitter:callback')

    def get_setup_callback_url(self):
        return reverse('langkawi:twitter:setup')
    
    def get_redirect_mock_response(self, *args, **kwargs):
        return {'status': '200'}, urllib.urlencode({
            'oauth_token': '123',
            'oauth_token_secret': '456'})
    
    def get_callback_mock_response(self, *args, **kwargs):
        return {'status': '200'}, urllib.urlencode({
            'oauth_token': '456',
            'oauth_token_secret': '789',
            'user_id': '123'})
    
    def get_setup_callback_mock_response(self, *args, **kwargs):
        return {'status': '200'}, urllib.urlencode({})
    
    def create_profile(self, user):
        TwitterProfile.objects.create(user=user, twitter_id='123')


class TestAuthenticationBackend(TestCase):
    def test_authentication_backend_should_be_configured_in_settings(self):
        self.assertTrue('langkawi.contrib.twitter.auth.TwitterAuth' in settings.AUTHENTICATION_BACKENDS)
