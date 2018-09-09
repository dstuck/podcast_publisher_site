from __future__ import unicode_literals

from django.db import models
import datetime as dt


class OAuthKey(models.Model):
    access_token = models.CharField(max_length=100)
    expires_at = models.DateTimeField()
    refresh_token = models.CharField(max_length=100, default='')
    scope = models.CharField(max_length=200)
    token_type = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def create(cls, **kwargs):
        expires_at = dt.datetime.utcnow() + dt.timedelta(
            seconds=int(kwargs.pop('expires_in'))
        )
        kwargs['expires_at'] = expires_at
        return cls(**kwargs)
