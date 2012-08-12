from django.conf import settings
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from socialregistration.clients.oauth import OAuth2
from socialregistration.settings import SESSION_KEY
import json
from pprint import pprint


class Weibo(OAuth2):
    client_id = getattr(settings, 'WEIBO_CLIENT_ID', '')
    secret = getattr(settings, 'WEIBO_CLIENT_SECRET', '')
    scope = getattr(settings, 'WEIBO_REQUEST_PERMISSIONS', '')
    site = 'https://api.weibo.com/'
    auth_url = 'oauth2/authorize'
    access_token_url = 'oauth2/access_token'
    api_url = 'https://api.weibo.com/2/'
    upload_api_url = 'https://upload.api.weibo.com/2/'
    _user_info = None

    def get_callback_url(self):
        if self.is_https():
            return 'https://%s%s' % (Site.objects.get_current().domain,
                reverse('socialregistration:weibo:callback'))
        return 'http://%s%s' % (Site.objects.get_current().domain,
            reverse('socialregistration:weibo:callback'))

    def get_access_token(self, **params):
        return super(Weibo, self).get_access_token(**params)

    def parse_access_token(self, content):
        return json.loads(content)

    def get_user_info(self):
        if self._user_info is None:
            #content = self.request('https://api.weibo.com/2/account/get_uid.json')
            content = self.r_get('account/get_uid.json')
            uid = content.json['uid']
            self._user_info = uid
            pprint(self._user_info)
        return self._user_info

    def send(self, status, filename=None):
        data = {'status': status}
        if filename is None:
            return self.r_post('statuses/update.json', data=data)
        pic = {'pic': open(filename, 'rb')}
        return self.r_upload('statuses/upload.json', pic, data=data)

    @staticmethod
    def get_session_key():
        return '%sweibo' % SESSION_KEY
