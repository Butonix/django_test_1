from django.db import models
from django.conf import settings


class Post(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.CharField(max_length=128)
    text = models.CharField(max_length=1024)


class Feed(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    post = models.ForeignKey(Post)
    read = models.IntegerField()


class Subscribers(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    subscriber = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='subs')