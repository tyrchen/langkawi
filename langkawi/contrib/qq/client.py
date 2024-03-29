from django.conf import settings
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from langkawi.clients.oauth import OAuth2
from langkawi.settings import SESSION_KEY
import re
import json


class QQ(OAuth2):
    client_id = getattr(settings, 'QQ_CLIENT_ID', '')
    secret = getattr(settings, 'QQ_CLIENT_SECRET', '')
    scope = getattr(settings, 'QQ_REQUEST_PERMISSIONS', '')
    site = 'https://graph.qq.com/'
    auth_url = 'oauth2.0/authorize'
    access_token_url = 'oauth2.0/token'
    expires_in = 30 * 24 * 3600
    _uid = None
    _user_info = None

    def get_callback_url(self):
        if self.is_https():
            return '%s%s' % (Site.objects.get_current().domain,
                reverse('langkawi:qq:callback'))
        return '%s%s' % (Site.objects.get_current().domain,
            reverse('langkawi:qq:callback'))

    def get_access_token(self, **params):
        params['grant_type'] = 'authorization_code'
        #params['state'] = 'tukeq'
        return super(QQ, self).get_access_token(**params)

    def parse_access_token(self, content):
        return json.loads(content)

    def get_user_info(self):
        if self._uid is None:
            request_get_me = self.request('https://graph.qq.com/oauth2.0/me')
            patt = '\{.*\}'
            m = re.search(patt, request_get_me.text)
            if m is not None:
                openid = json.loads(m.group())['openid']
                self._uid = {'openid': openid}
                params = {'oauth_consumer_key': self.client_id, 'openid': openid}
                user_info = self.request('https://graph.qq.com/user/get_user_info', params=params).json
                self._user_info = {}
                self._user_info.update(self._uid)
                self._user_info['name'] = user_info['nickname']
                self._user_info['gender'] = user_info['gender']
                self._user_info['profile_image_url'] = user_info['figureurl_2']
        return self._uid, self._user_info

    def create_friendships(self, user, profile):
        pass

    def send(self, status, filename=None):
        data = {'content': status}
        if filename is None:
            return self.r_post('statuses/update.json', data=data)
        pic = {'pic': open(filename, 'rb')}
        return self.r_upload('statuses/upload.json', pic, data=data)

    @staticmethod
    def get_session_key():
        return '%sqq' % SESSION_KEY
