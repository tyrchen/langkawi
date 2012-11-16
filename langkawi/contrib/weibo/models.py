from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.db import models
from langkawi.signals import connect


class WeiboProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    site = models.ForeignKey(Site, default=Site.objects.get_current)
    weibo_uid = models.CharField(max_length=50)
    screen_name = models.CharField(max_length=50, blank=True, default='')
    name = models.CharField(max_length=50, blank=True, default='')
    location = models.CharField(max_length=50, blank=True, default='')
    description = models.CharField(max_length=255, blank=True, default='')
    gender = models.CharField(max_length=1, blank=True, default='m')
    profile_image_url = models.URLField(blank=True, default='')

    class Meta:
        db_table = 'social_weiboprofile'

    def __unicode__(self):
        try:
            return u'%s: %s' % (self.user, self.weibo_uid)
        except User.DoesNotExist:
            return u'None'

    def authenticate(self):
        return authenticate(weibo_uid=self.weibo_uid)


class WeiboAccessToken(models.Model):

    profile = models.OneToOneField(WeiboProfile, related_name='access_token')
    access_token = models.CharField(max_length=255)
    token_expires_in = models.IntegerField()

    class Meta:
        db_table = 'social_weiboaccesstoken'


def save_weibo_token(sender, user, profile, client, **kwargs):
    try:
        WeiboAccessToken.objects.get(profile=profile).delete()
    except WeiboAccessToken.DoesNotExist:
        pass

    WeiboAccessToken.objects.create(access_token=client.get_access_token(),
        profile=profile, token_expires_in=client.token_expires_in)


connect.connect(save_weibo_token, sender=WeiboProfile,
    dispatch_uid='langkawi_weibo_token')
