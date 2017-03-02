from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

class Post(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.CharField(max_length=128)
    text = models.CharField(max_length=1024)
    date = models.DateTimeField(auto_now_add=True)


class Feed(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    post = models.ForeignKey(Post)
    read = models.IntegerField()


class Subscribers(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    subscriber = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='subs')


#Сигналы
    @receiver(post_save, sender=Post)
    def on_add_post(sender, **kwargs):

        if kwargs['created']:
            subs = Subscribers.objects.filter(user=kwargs['instance'].owner_id)
            print(subs)



