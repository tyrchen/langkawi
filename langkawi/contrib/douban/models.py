from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.db import models
from langkawi.signals import connect


class DoubanProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    site = models.ForeignKey(Site, default=Site.objects.get_current)
    douban = models.CharField(max_length=255)

    def __unicode__(self):
        try:
            return u'%s: %s' % (self.user, self.douban)
        except User.DoesNotExist:
            return u'None'

    def authenticate(self):
        return authenticate(douban=self.douban)


class DoubanAccessToken(models.Model):
    profile = models.OneToOneField(DoubanProfile, related_name='access_token')
    access_token = models.CharField(max_length=255)


def save_douban_token(sender, user, profile, client, **kwargs):
    try:
        DoubanAccessToken.objects.get(profile=profile).delete()
    except DoubanAccessToken.DoesNotExist:
        pass

    DoubanAccessToken.objects.create(access_token=client.get_access_token(),
        profile=profile)


connect.connect(save_douban_token, sender=DoubanProfile,
    dispatch_uid='langkawi_douban_token')
