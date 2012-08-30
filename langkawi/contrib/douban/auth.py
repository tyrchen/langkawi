from django.contrib.sites.models import Site
from langkawi.contrib.douban.models import DoubanProfile
from django.contrib.auth.backends import ModelBackend


class DoubanAuth(ModelBackend):
    def authenticate(self, douban=None):
        try:
            return DoubanProfile.objects.get(
                douban=douban,
                site=Site.objects.get_current()).user
        except DoubanProfile.DoesNotExist:
            return None
