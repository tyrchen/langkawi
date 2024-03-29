from django.conf import settings
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from langkawi.clients.oauth import OAuth2
from langkawi.settings import SESSION_KEY
import json


class Weibo(OAuth2):
    client_id = getattr(settings, 'WEIBO_CLIENT_ID', '')
    secret = getattr(settings, 'WEIBO_CLIENT_SECRET', '')
    scope = getattr(settings, 'WEIBO_REQUEST_PERMISSIONS', '')
    site = 'https://api.weibo.com/'
    auth_url = 'oauth2/authorize'
    access_token_url = 'oauth2/access_token'
    api_url = 'https://api.weibo.com/2/'
    upload_api_url = 'https://upload.api.weibo.com/2/'
    _uid = None
    _user_info = None

    def get_callback_url(self):
        if self.is_https():
            return '%s%s' % (Site.objects.get_current().domain,
                reverse('langkawi:weibo:callback'))
        return '%s%s' % (Site.objects.get_current().domain,
            reverse('langkawi:weibo:callback'))

    def get_access_token(self, **params):
        return super(Weibo, self).get_access_token(**params)

    def parse_access_token(self, content):
        return json.loads(content)

    def get_user_info(self):
        if self._uid is None:
            #fetch weibo uid
            get_uid_response = self.r_get('account/get_uid.json')
            self._uid = {'weibo_uid': get_uid_response.json['uid']}
            get_info_response = self.r_get('users/show.json', get_uid_response.json)
            user_info_dict = get_info_response.json
            keys = ['screen_name', 'name', 'location', 'description', 'gender', 'profile_image_url']
            self._user_info = {}
            self._user_info.update(self._uid)
            for key in keys:
                if key in user_info_dict:
                    self._user_info.update({key: user_info_dict.pop(key)})
        return self._uid, self._user_info

    def create_friendships(self, user, profile):
        #fetch & save user's friends relationship
        #pprint('weibo uid:%s' % profile.weibo_uid)
        get_friends_response = self.r_get('friendships/friends/bilateral.json', {'uid': profile.weibo_uid, 'count': 200})
        #pprint(get_friends_response.text)
        friends = get_friends_response.json['users']

    def send(self, status, filename=None):
        data = {'status': status}
        if filename is None:
            return self.r_post('statuses/update.json', data=data)
        pic = {'pic': open(filename, 'rb')}
        return self.r_upload('statuses/upload.json', pic, data=data)

    @staticmethod
    def get_session_key():
        return '%sweibo' % SESSION_KEY
