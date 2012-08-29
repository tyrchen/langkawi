from django.contrib.sites.models import Site
from langkawi.contrib.renren.models import RenrenProfile
from django.contrib.auth.backends import ModelBackend


class RenrenAuth(ModelBackend):
    def authenticate(self, renren=None):
        try:
            return RenrenProfile.objects.get(
                renren=renren,
                site=Site.objects.get_current()).user
        except RenrenProfile.DoesNotExist:
            return None
