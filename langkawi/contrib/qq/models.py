#-*- coding:utf-8 -*-
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.db import models
from langkawi.signals import connect
from langkawi.models import BaseProfile

class QQProfile(BaseProfile):

    openid = models.CharField(max_length=100)
    name = models.CharField(max_length=50, default='', blank=True)
    gender = models.CharField(max_length=10,default='', blank=True)

    class Meta:
        db_table = 'social_qqprofile'

    def __unicode__(self):
        try:
            return u'%s: %s' % (self.user, self.openid)
        except User.DoesNotExist:
            return u'None'

    def authenticate(self):
        return authenticate(openid=self.openid)


class QQAccessToken(models.Model):

    profile = models.OneToOneField(QQProfile, related_name='access_token')
    access_token = models.CharField(max_length=255)
    token_expires_in = models.IntegerField()

    class Meta:
        db_table = 'social_qqaccesstoken'


def save_qq_token(sender, user, profile, client, **kwargs):
    try:
        QQAccessToken.objects.get(profile=profile).delete()
    except QQAccessToken.DoesNotExist:
        pass

    QQAccessToken.objects.create(access_token=client.get_access_token(),
        profile=profile, token_expires_in=client.token_expires_in)


connect.connect(save_qq_token, sender=QQProfile,
    dispatch_uid='langkawi_qq_token')
