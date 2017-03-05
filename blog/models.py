from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.CharField(max_length=128)
    text = models.CharField(max_length=1024)
    date = models.DateTimeField(auto_now_add=True)


class Feed(models.Model):

    post = models.ForeignKey(Post)
    is_read = models.BooleanField()
    subscriber = models.ForeignKey(settings.AUTH_USER_MODEL)

# не использую ManyToMany поскольку не хочу изменять дефолтную модель User
class Subscribers(models.Model):
    blog = models.ForeignKey(settings.AUTH_USER_MODEL)
    subscriber = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='subs')

    class Meta:
        unique_together = ('blog', 'subscriber')


# Сигналы
# Поскольку всеравно нужно делать оповещение по почте, заодно обновляю ленты подписчиков
#   вместо того, что бы генерировать ленты по запросу
@receiver(post_save, sender=Post)
def on_add_post(sender, **kwargs):

    if kwargs['created']:
        post = kwargs['instance']
        subs_list = Subscribers.objects.filter(blog=post.author)
        print('======================')
        print('Отправка писем: ')

        for subs in subs_list:
            if subs.subscriber.email:
                print('mail to {} email: {}'.format(subs.subscriber.username,
                                                    subs.subscriber.email))
            print(subs.subscriber)
            Feed(post=post, subscriber=subs.subscriber, is_read=False).save()






