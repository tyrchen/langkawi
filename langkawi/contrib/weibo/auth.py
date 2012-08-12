from django.contrib.sites.models import Site
from socialregistration.contrib.weibo.models import WeiboProfile
from django.contrib.auth.backends import ModelBackend


class WeiboAuth(ModelBackend):
    def authenticate(self, weibo=None):
        try:
            return WeiboProfile.objects.get(
                weibo=weibo,
                site=Site.objects.get_current()).user
        except WeiboProfile.DoesNotExist:
            return None
