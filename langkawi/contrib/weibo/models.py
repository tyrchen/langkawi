from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.db import models
from socialregistration.signals import connect


class WeiboProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    site = models.ForeignKey(Site, default=Site.objects.get_current)
    weibo = models.CharField(max_length=255)

    def __unicode__(self):
        try:
            return u'%s: %s' % (self.user, self.weibo)
        except User.DoesNotExist:
            return u'None'

    def authenticate(self):
        return authenticate(weibo=self.weibo)


class WeiboAccessToken(models.Model):
    profile = models.OneToOneField(WeiboProfile, related_name='access_token')
    access_token = models.CharField(max_length=255)


def save_weibo_token(sender, user, profile, client, **kwargs):
    try:
        WeiboAccessToken.objects.get(profile=profile).delete()
    except WeiboAccessToken.DoesNotExist:
        pass

    WeiboAccessToken.objects.create(access_token=client.get_access_token(),
        profile=profile)


connect.connect(save_weibo_token, sender=WeiboProfile,
    dispatch_uid='socialregistration_weibo_token')
