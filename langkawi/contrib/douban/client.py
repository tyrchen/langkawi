from django.conf import settings
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from langkawi.clients.oauth import OAuth2
from langkawi.settings import SESSION_KEY
import json
from pprint import pprint


class Douban(OAuth2):
    client_id = getattr(settings, 'DOUBAN_CLIENT_ID', '')
    secret = getattr(settings, 'DOUBAN_CLIENT_SECRET', '')
    scope = getattr(settings, 'DOUBAN_REQUEST_PERMISSIONS', '')
    site = 'https://www.douban.com/service/'
    auth_url = 'auth2/auth'
    access_token_url = 'auth2/token'
    api_url = 'https://api.douban.com/v2/'
    expires_in = 30 * 24 * 3600
    _uid = None
    _user_info = None

    def get_callback_url(self):
        if self.is_https():
            return 'https://%s%s' % (Site.objects.get_current().domain,
                reverse('langkawi:douban:callback'))
        return 'http://%s%s' % (Site.objects.get_current().domain,
            reverse('langkawi:douban:callback'))

    def get_access_token(self, **params):
        params['grant_type'] = 'authorization_code'
        return super(Douban, self).get_access_token(**params)

    def parse_access_token(self, content):
        return json.loads(content)

    def request_api(self, api, method='GET'):
        headers = {"Authorization": "Bearer " + self.get_access_token()}
        if method == 'POST':
            return self.r_post(api, headers=headers)
        return self.r_get(api, headers=headers)

    def get_user_info(self):
        if self._uid is None:
            response = self.request_api('user/~me').json
            self._uid = {'uid': response['id']}
            self._user_info = {'name': response['name'],
            'domain': response['uid'],
            'profile_image_url': response['avatar'],
            'desc': response['desc']}
            self._user_info.update(self._uid)
            pprint(self._user_info)
        return self._uid, self._user_info

    def create_friendships(self, user, profile):
        pass

    def send(self, status, filename=None):
        pass

    @staticmethod
    def get_session_key():
        return '%sdouban' % SESSION_KEY
