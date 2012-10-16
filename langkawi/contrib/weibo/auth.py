from django.contrib.sites.models import Site
from langkawi.contrib.weibo.models import WeiboProfile
from django.contrib.auth.backends import ModelBackend
from langkawi.auth import LKWBackend

class WeiboAuth(LKWBackend):
    def authenticate(self, weibo_uid=None):
        try:
            return WeiboProfile.objects.get(
                weibo_uid=weibo_uid,
                site=Site.objects.get_current()).user
        except WeiboProfile.DoesNotExist:
            return None

